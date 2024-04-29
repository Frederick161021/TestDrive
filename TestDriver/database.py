import mysql.connector

class Database:
    __instance = None

    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        Database.__instance = self
        self.connection = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="testdriver"
        )

    def get_connection(self):
        return self.connection
