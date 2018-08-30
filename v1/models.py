import psycopg2
import os 
from v1 import env

'''creating tables'''
class Database:
    def __init__(self):
        if env == 'testing':
            self.conn = psycopg2.connect(
                host=os.environ.get('HOST'),
                user=os.environ.get('DBUSER'),
                password=os.environ.get('PASSWORD'),
                dbname=os.environ.get('TESTDB')
                )
        elif env == "production":
            self.conn = psycopg2.connect(
                host='ec2-54-235-160-57.compute-1.amazonaws.com',
                user='dejkpzjbrysvkp',
                password='e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403',
                dbname="df3terog2vbq3c",
                port='5432'
                )
        else:
            self.conn = psycopg2.connect(
                host=os.environ.get('HOST'),
                user=os.environ.get('DBUSER'),
                password=os.environ.get('PASSWORD'),
                dbname=os.environ.get('DATABASE')
                )

        self.conn.autocommit = True
        self.c = self.conn.cursor()
        
    def create_table(self):
        commands=(
         
            '''CREATE TABLE IF NOT EXISTS users(
                email VARCHAR(100) PRIMARY KEY NOT NULL UNIQUE,
                username       VARCHAR(50),
                password VARCHAR(100)
            )''',
            ''' CREATE TABLE IF NOT EXISTS entries(
                    email VARCHAR(100),
                    entry_id SERIAL PRIMARY KEY,
                    title VARCHAR(100),
                    date VARCHAR(50),
                    content VARCHAR,
                    FOREIGN KEY (email)
                    REFERENCES users (email)
                    ON UPDATE CASCADE ON DELETE CASCADE
                    
                )''',
                ''' CREATE TABLE IF NOT EXISTS notifications(
                    email VARCHAR(100),
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100),
                    date VARCHAR(50),
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
class User(Database):
    def __init__(self, email,username, password):
        Database.__init__(self)
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
        command ="SELECT * FROM users WHERE email = %s "
        self.c.execute(command,(self.email,))
        value=self.c.fetchone()
        return value
   
'''methods for the entry class'''        
class Entry:
    def __init__(self,email, title,date,content):
        Database.__init__(self)
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
    ''' deleting an entry '''

    def delete_entry(self,entry_id):
        command = "DELETE FROM entries WHERE entry_id = %s"
        self.c.execute(command,(entry_id,))
class Notifications:
    def __init__(self,email, title,date):
        Database.__init__(self)
        self.email = email
        self.title = title
        self.date = date
    def add_reminder(self):
        command = '''INSERT INTO notifications (email,title, date)
        VALUES (%s, %s, %s)'''
        self.c.execute(command, (self.email,self.title, self.date))
    
    def get_reminder(self):
        command = "SELECT * FROM notifications WHERE email = %s "
        self.c.execute(command,(self.email,))
        value=self.c.fetchall()
        return value

db=Database()



       



  