from pika import BlockingConnection, ConnectionParameters
from mongoengine import connect
import json
import time
from contact_model import Contact

connect("MongoTest", host="mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')


# Функція для імітації надсилання повідомлення по електронній пошті
def simulate_email_send(contact_id):
    # Імітація надсилання повідомлення (через засіб time.sleep)
    print(f"Simulating email send for contact with ID {contact_id}")
    time.sleep(2)  # Імітуємо 2 секунди надсилання
    print(f"Email sent for contact with ID {contact_id}")

    # Зміна значення логічного поля для контакту на True
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()


# Функція для обробки отриманих повідомлень з черги
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    if contact_id:
        simulate_email_send(contact_id)
    else:
        print("Invalid message format. Missing contact_id.")


# Обробка повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()