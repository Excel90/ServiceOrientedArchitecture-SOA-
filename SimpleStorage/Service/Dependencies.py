import re
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import os

import configparser


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
            
            self.connection.close()
            return "Login Failed user not found"
    
    def check_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def register(self,name,email, username, password):
        cursor = self.connection.cursor()
        if self.check_username(username):
            
            self.connection.close()
            return "Username already exists"
        else:
            cursor.execute("INSERT INTO users (nama, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))
            self.connection.commit()
            os.makedirs(f"Storage/{username}")
            write_config = configparser.ConfigParser()
            write_config.add_section('Folder_Owner')
            write_config['Folder_Owner']['Name'] = username
            write_config.add_section('Shared_folder')
            config_folder = os.path.join(f"Storage/{username}/config.ini")
            cfgfile = open(config_folder, 'w')
            write_config.write(cfgfile)
            cfgfile.close()
            return "Register Success"
        

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

    