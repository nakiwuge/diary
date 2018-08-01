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
                email VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
                username       VARCHAR(50),
                password VARCHAR(50)
            )''',
            ''' CREATE TABLE IF NOT EXISTS entries(
                    email VARCHAR(50),
                    entry_id SERIAL PRIMARY KEY,
                    title VARCHAR(50),
                    date VARCHAR(50),
                    content VARCHAR(50),
                    FOREIGN KEY (email)
                    REFERENCES users (email)
                    ON UPDATE CASCADE ON DELETE CASCADE
                    
                )'''
            
            )
            
        for command in commands:
            self.c.execute(command)

class User:
    def __init__(self, email,username, password):
        self.username=username
        self.email=email
        self.password=password

    def add_user(self):
        command = '''INSERT INTO users (email, username, password)
        VALUES (%s, %s, %s)
        '''
       
        c.execute(command, (self.email, self.username, self.password))

    def login_user(self):
        command ="SELECT email FROM users WHERE email = %s AND password=%s"
        c.execute(command,(self.email, self.password))
        value=c.fetchone()
        return value
        
class Entry:
    def __init__(self,email, title,date,content):
        self.email= email
        self.title = title
        self.date = date
        self.content = content

    def add_entry(self):
        command = '''INSERT INTO entries (email,title, date, content)
        VALUES (%s, %s, %s, %s)
        '''
        c.execute(command, (self.email,self.title, self.date, self.content))
    
    def get_all_entries(self):
        command = "SELECT * FROM entries WHERE email = %s "
        c.execute(command,(self.email,))
        value=c.fetchall()
        return value
    @staticmethod   
    def get_entry_by_id(entry_id):
        command = "SELECT * FROM entries WHERE entry_id = %s "
        c.execute(command,[entry_id])
        value = c.fetchone()
        return value




       



  