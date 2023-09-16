from mongoengine import Document, StringField, BooleanField, EmailField


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone_number = StringField()
    contact_method = StringField(choices=["email", "sms"])
    message_sent = BooleanField(default=False)

    def __str__(self):
        return f"Contact: {self.full_name} ({self.email})"