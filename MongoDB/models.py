import mongoengine as db


class Author(db.Document):
    fullname = db.StringField(required=True)
    born_date = db.StringField()
    born_location = db.StringField()
    description = db.StringField()


class Quote(db.Document):
    tags = db.ListField(db.StringField())
    author = db.ReferenceField(Author)
    quote = db.StringField()