from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        result = cursor.fetchone()
        json = {
            "id": result[0],
            "name": result[1],
            "email": result[2]
        }
        if result != "":
            return json
        else:
            self.connection.close()
            return {"Login": "Email or password is incorrect"}

    def register(self, name, email, password):
        cursor = self.connection.cursor()
        if self.check_email(email):
            self.connection.close()
            return {"Register": "Email already exists"}
        else:
            cursor.execute("INSERT INTO users (nama, email, password) VALUES (%s, %s, %s)", (name, email, password))
            self.connection.commit()
            return {"Register": "Successs"}

    def check_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    
    def insertnews(self, title, content, attachment, author):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO news (news_title, news_content, attachment,news_author) VALUES (%s, %s, %s, %s)", (title, content, attachment,author))
            self.connection.commit()
            return {"Insert": "Success"}
        except Error as e:
            return e
        finally:
            self.connection.close()

    def getnews(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news JOIN users ON news.news_author = users.id")
        result = cursor.fetchall()
        data = []
        for row in result:
            data.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "attachment": row[3],
                "date": row[4],
                "author": row[7]
            })
        return data

    def getnewsbyid(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news JOIN users ON news.news_author = users.id WHERE news.id = %s", (id,))
        result = cursor.fetchone()
        json = {
            "id": result[0],
            "title": result[1],
            "content": result[2],
            "attachment": result[3],
            "date": result[4],
            "author": result[7]
        }
        return json
    
    def getnewsattach(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT attachment FROM news WHERE id = %s", (id,))
        result = cursor.fetchone()
        json = {
            "attachment": result[0]
        }
        return json

    def updatenewattachment(self, file_path, id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE news SET attachment = %s WHERE id = %s", (file_path, id))
        self.connection.commit()
        return {"Update": "Success"}

    def updatenews(self, title, content, id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE news SET news_title = %s, news_content = %s WHERE id = %s", (title, content, id))
        self.connection.commit()
        return {"Update": "Success"}

    def deletenews(self, id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM news WHERE id = %s", (id,))
        self.connection.commit()
        return {"Delete": "Success"}

    def __del__(self):
        self.connection.close()

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='127.0.0.1',
                database='news_board',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())

    