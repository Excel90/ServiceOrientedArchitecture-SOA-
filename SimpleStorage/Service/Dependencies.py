from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import os


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result != "":
            return result
        else:
            return "Login Failed user not found"
    
    def register(self,name,email, username, password):
        cursor = self.connection.cursor()

        try:
            cursor.execute("INSERT INTO users (nama, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))
            self.connection.commit()
            os.makedirs(f"Storage/{username}")
            return "Register Success"
        except Error as e:
            return e
        finally:
            return "User Already Exists"

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='127.0.0.1',
                database='cloud_storage',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())

    