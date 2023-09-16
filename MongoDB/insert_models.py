import json
from mongoengine import connect
from models import Author, Quote


connect("MongoTest", host="mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")

with open("authors.json", "r") as authors_file:
    authors_json_data = json.load(authors_file)

with open("quotes.json", "r") as quotes_file:
    quotes_json_data = json.load(quotes_file)

for author_data in authors_json_data:
    author = Author(**author_data)
    author.save()

for quote_data in quotes_json_data:
    author_fullname = quote_data['author']
    author = Author.objects(fullname=author_fullname).first()

    if author:
        del quote_data['author']
        quote = Quote(author=author, **quote_data)
        quote.save()
    else:
        print(f"Автор з ім'ям '{author_fullname}' не знайдений.")