from pika import BlockingConnection, ConnectionParameters
from mongoengine import connect
from faker import Faker
import json
from contact_model import Contact

# Підключення до MongoDB за допомогою URI
connect("MongoTest", host="mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

# Підключення до сервера RabbitMQ
connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')


def send_contacts_to_queue(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()

        # Визначаємо випадковий спосіб надсилання для контакту (email або sms)
        contact_method = fake.random_element(elements=("email", "sms"))

        # Створення об'єкта контакту і збереження його в базі даних
        contact = Contact(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            contact_method=contact_method
        )
        contact.save()

        # Відправка повідомлення до відповідної черги
        message = {
            'contact_id': str(contact.id),
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'contact_method': contact_method
        }

        if contact_method == "sms":
            channel.basic_publish(exchange='', routing_key='sms_queue', body=json.dumps(message))
            print(f" [x] Sent SMS contact with ID {contact.id} to the SMS queue")
        elif contact_method == "email":
            channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))
            print(f" [x] Sent email contact with ID {contact.id} to the email queue")


if __name__ == "__main__":
    num_contacts_to_generate = 20
    send_contacts_to_queue(num_contacts_to_generate)
    connection.close()


