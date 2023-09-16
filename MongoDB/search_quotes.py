from pymongo import MongoClient
from bson import ObjectId

client = MongoClient(
    "mongodb+srv://andreyvlasiuk1991:w0lD0A1Q9V2OStNJ@cluster0.ldbtewo.mongodb.net/test?retryWrites=true&w=majority")
db = client["MongoTest"]


# Функція для пошуку цитат за тегом
def search_quotes_by_tag(tag):
    quotes_collection = db["quotes"]
    result = quotes_collection.find({"tags": tag})
    return list(result)


# Функція для пошуку цитат за іменем автора
def search_quotes_by_author(author_name):
    quotes_collection = db["quotes"]
    result = quotes_collection.find({"author": author_name})
    return list(result)


# Функція для пошуку цитат за набором тегів
def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes_collection = db["quotes"]
    result = quotes_collection.find({"tags": {"$in": tags_list}})
    return list(result)


while True:
    command = input("Введіть команду (наприклад, 'name: Steve Martin', 'tag: life', 'tags: life,live', 'exit'): ")

    if command.startswith("name: "):
        author_name = command[len("name: "):].strip()
        quotes = search_quotes_by_author(author_name)
        print("Результат пошуку за іменем автора:")
        for quote in quotes:
            print(f"Цитата: {quote['quote']}".encode('utf-8').decode('utf-8'))

    elif command.startswith("tag: "):
        tag = command[len("tag: "):].strip()
        quotes = search_quotes_by_tag(tag)
        print("Результат пошуку за тегом:")
        for quote in quotes:
            print(f"Цитата: {quote['quote']}".encode('utf-8').decode('utf-8'))

    elif command.startswith("tags: "):
        tags = command[len("tags: "):].strip()
        quotes = search_quotes_by_tags(tags)
        print("Результат пошуку за набором тегів:")
        for quote in quotes:
            print(f"Цитата: {quote['quote']}".encode('utf-8').decode('utf-8'))

    elif command == "exit":
        print("Завершення роботи скрипту.")
        break

    else:
        print("Невідома команда. Введіть коректну команду або 'exit' для завершення.")
