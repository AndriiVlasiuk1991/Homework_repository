import json
from pymongo import MongoClient


client = MongoClient("mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/test?retryWrites=true&w=majority")
db = client["MongoTest"]


with open("authors.json", "r") as authors_file:
    authors_data = json.load(authors_file)

authors_collection = db["authors"]
authors_collection.insert_many(authors_data)

with open("quotes.json", "r") as quotes_file:
    quotes_data = json.load(quotes_file)

quotes_collection = db["quotes"]
quotes_collection.insert_many(quotes_data)