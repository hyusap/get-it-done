import sqlite3
from sqlite3 import Error


class database:
    connection = None

    def __init__(self, path='database/main.db'):
        try:
            self.connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def read(self, *args):
        cursor = self.connection.cursor()
        try:
            cursor.execute(*args)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def close(self):
        self.connection.close()


def db_read(*args):
    db = database('database/main.db')
    data = db.read(*args)
    db.close()
    return data
