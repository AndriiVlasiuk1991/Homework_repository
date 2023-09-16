from pika import BlockingConnection, ConnectionParameters
from mongoengine import connect
import json
from contact_model import Contact


connect("MongoTest", host="mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черги для SMS-повідомлень
channel.queue_declare(queue='sms_queue')


# Функція для обробки контактів по SMS
def process_sms_contact(contact_id):
    contact = Contact.objects(id=contact_id, contact_method="sms").first()
    if contact:
        print(f"Processing SMS for contact with ID {contact_id}")
        contact.message_sent = True
        contact.save()
        print(f"SMS sent for contact with ID {contact_id}")
    else:
        print(f"SMS contact with ID {contact_id} not found")


def sms_callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    process_sms_contact(contact_id)


# Підписка на чергу для SMS
channel.basic_consume(queue='sms_queue', on_message_callback=sms_callback, auto_ack=True)

print(" [*] Waiting for SMS messages. To exit press CTRL+C")
channel.start_consuming()
