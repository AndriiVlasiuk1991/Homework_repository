from pika import BlockingConnection, ConnectionParameters
from mongoengine import connect
import json
from contact_model import Contact

connect("MongoTest",
        host="mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги для email-повідомлень
channel.queue_declare(queue='email_queue')


# Функція для обробки контактів по email
def process_email_contact(contact_id):
    contact = Contact.objects(id=contact_id, contact_method="email").first()
    if contact:
        print(f"Processing email for contact with ID {contact_id}")
        contact.message_sent = True
        contact.save()
        print(f"Email sent for contact with ID {contact_id}")
    else:
        print(f"Email contact with ID {contact_id} not found")


def email_callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    process_email_contact(contact_id)


# Підписка на чергу для email
channel.basic_consume(queue='email_queue', on_message_callback=email_callback, auto_ack=True)

print(" [*] Waiting for email messages. To exit press CTRL+C")
channel.start_consuming()
