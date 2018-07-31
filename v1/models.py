from flask import jsonify
from v1 import conn,c,dict_cur

class CreateTables:
    def __init__(self):
        self.c=c
        self.conn=conn
        self.conn.autocommit=True
    def create_table(self):
        commands=(
         
            '''CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50),
                email       VARCHAR(50),
                password VARCHAR(50)
            )''',
            ''' CREATE TABLE IF NOT EXISTS entries(
                    entry_id SERIAL PRIMARY KEY,
                    title VARCHAR(50),
                    date VARCHAR(50),
                    content VARCHAR(50)
                    
                )'''
            
            )
            
        for command in commands:
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
        
class Entry:
    def __init__(self, title,date,content):
        self.title = title
        self.date = date
        self.content = content

    def add_entry(self):
        command = '''INSERT INTO entries (title, date, content)
        VALUES (%s, %s, %s)
        '''
        c.execute(command, (self.title, self.date, self.content))
    @staticmethod
    def get_all_entries():
        command = '''SELECT * FROM entries'''
        c.execute(command)
        value=c.fetchall()
        return value
        




       



  