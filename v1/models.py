from flask import jsonify
from v1 import conn,c

class CreateTables:
    def __init__(self):
        self.c=c
        self.conn=conn
        self.conn.autocommit=True
    def create_user_table(self):
        command=(
         
            '''CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50),
                email       VARCHAR(50),
                password VARCHAR(50)
            )'''
            )

        self.c.execute(command)

class User:
    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password

    def add_user(self):
        command = '''INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        '''
       
        c.execute(command, (self.username, self.email, self.password))

    def login_user(self):
        command ="SELECT username FROM users WHERE email = %s AND password=%s"
        c.execute(command,(self.email, self.password))
        value=c.fetchone()
        return value
        
       
        




       



  