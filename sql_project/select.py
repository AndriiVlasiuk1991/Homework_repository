import sqlite3


def execute_query(query: str):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        with open(query, 'r') as file:
            sql = file.read()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == '__main__':
    for n in range(1, 13):
        print(execute_query(f'query_{n}.sql'))
