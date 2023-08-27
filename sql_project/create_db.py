import sqlite3


def create_db():
    # читаємо файл зі скриптом для створення БД
    with open('salary.sql', 'r') as file:
        sql_script = file.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        # виконуємо скрипт із файлу, який створить таблиці в БД
        cur.executescript(sql_script)

if __name__ == '__main__':
    create_db()
