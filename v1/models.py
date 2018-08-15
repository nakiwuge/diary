import psycopg2
from v1 import app
'''creating tables'''
class Database:
    def __init__(self):
      
        self.conn = psycopg2.connect(
            host='ec2-54-235-160-57.compute-1.amazonaws.com',
            user='dejkpzjbrysvkp',
            password='e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403',
            dbname='df3terog2vbq3c',
            port='5432',
            uri='postgres://dejkpzjbrysvkp:e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403@ec2-54-235-160-57.compute-1.amazonaws.com:5432/df3terog2vbq3c'
    )
        self.conn.autocommit = True
        self.c = self.conn.cursor()
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

    def delete_tables(self):
        command = "DROP TABLE entries, users"
        
        self.c.execute(command)

''' methods for the user class'''
class User:
    def __init__(self, email,username, password):
     
        self.conn = psycopg2.connect(
            host='ec2-54-235-160-57.compute-1.amazonaws.com',
            user='dejkpzjbrysvkp',
            password='e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403',
            dbname='df3terog2vbq3c',
            port='5432',
            uri='postgres://dejkpzjbrysvkp:e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403@ec2-54-235-160-57.compute-1.amazonaws.com:5432/df3terog2vbq3c'
    )
        self.conn.autocommit = True
        self.c = self.conn.cursor()
        self.username=username
        self.email=email
        self.password=password
    ''' Adding a user'''
    def add_user(self):
        command = '''INSERT INTO users (email, username, password)
        VALUES (%s, %s, %s)'''
        self.c.execute(command, (self.email, self.username, self.password))
    ''' check for duplicate emails'''
    def check_duplicate(self):
        command = "SELECT email FROM users where email = %s"
        self.c.execute(command,(self.email,))
        value = self.c.fetchone()
        return value
    ''' loggin a user '''
    def login_user(self):
        command ="SELECT email FROM users WHERE email = %s AND password=%s"
        self.c.execute(command,(self.email, self.password))
        value=self.c.fetchone()
        return value

'''methods for the entry class'''        
class Entry:
    def __init__(self,email, title,date,content):
        
        self.conn = psycopg2.connect(
            host='ec2-54-235-160-57.compute-1.amazonaws.com',
            user='dejkpzjbrysvkp',
            password='e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403',
            dbname='df3terog2vbq3c',
            port='5432',
            uri='postgres://dejkpzjbrysvkp:e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403@ec2-54-235-160-57.compute-1.amazonaws.com:5432/df3terog2vbq3c'
    )
        self.conn.autocommit = True
        self.c = self.conn.cursor()
        self.email = email
        self.title = title
        self.date = date
        self.content = content
    ''' adding an entry'''
    def add_entry(self):
        command = '''INSERT INTO entries (email,title, date, content)
        VALUES (%s, %s, %s, %s)
        '''
        self.c.execute(command, (self.email,self.title, self.date, self.content))
    ''' getting all entries'''
    def get_all_entries(self):
        command = "SELECT * FROM entries WHERE email = %s "
        self.c.execute(command,(self.email,))
        value=self.c.fetchall()
        return value
    ''' getting a specific entry'''
    def get_entry_by_id(self,entry_id):
        command = "SELECT * FROM entries WHERE entry_id = %s and email = %s "
        self.c.execute(command,(entry_id,self.email))
        value = self.c.fetchone()
        return value
    ''' modifying an entry '''
    def modify_entry(self, entry_id):
        command = "UPDATE entries SET title = %s , content = %s WHERE entry_id = %s  "
        self.c.execute(command, (self.title, self.content, entry_id))
    ''' checking entries with same title '''   
    def check_entry_duplicate(self):
        command = "SELECT title FROM entries where email = %s"
        self.c.execute(command,(self.email,))
        value =self.c.fetchall()
        return value
    

db=Database()



       



  