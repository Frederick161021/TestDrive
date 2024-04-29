import mysql.connector

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="",
                database="testdriver"
            )
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor.fetchall()
        finally:
            cursor.close()
            self.close_connection()
