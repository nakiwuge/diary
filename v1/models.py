
from v1 import c
from v1.config import Config

'''creating tables'''
class Database:
    def __init__(self):
        self.c = c
        self.conn = Config.conn
        self.conn.autocommit = True
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
        self.username=username
        self.email=email
        self.password=password
    ''' Adding a user'''
    def add_user(self):
        command = '''INSERT INTO users (email, username, password)
        VALUES (%s, %s, %s)'''
        c.execute(command, (self.email, self.username, self.password))
    ''' check for duplicate emails'''
    def check_duplicate(self):
        command = "SELECT email FROM users where email = %s"
        c.execute(command,(self.email,))
        value = c.fetchone()
        return value
    ''' loggin a user '''
    def login_user(self):
        command ="SELECT email FROM users WHERE email = %s AND password=%s"
        c.execute(command,(self.email, self.password))
        value=c.fetchone()
        return value

'''methods for the entry class'''        
class Entry:
    def __init__(self,email, title,date,content):
        self.email = email
        self.title = title
        self.date = date
        self.content = content
    ''' adding an entry'''
    def add_entry(self):
        command = '''INSERT INTO entries (email,title, date, content)
        VALUES (%s, %s, %s, %s)
        '''
        c.execute(command, (self.email,self.title, self.date, self.content))
    ''' getting all entries'''
    def get_all_entries(self):
        command = "SELECT * FROM entries WHERE email = %s "
        c.execute(command,(self.email,))
        value=c.fetchall()
        return value
    ''' getting a specific entry'''
    def get_entry_by_id(self,entry_id):
        command = "SELECT * FROM entries WHERE entry_id = %s and email = %s "
        c.execute(command,(entry_id,self.email))
        value = c.fetchone()
        return value
    ''' modifying an entry '''
    def modify_entry(self, entry_id):
        command = "UPDATE entries SET title = %s , content = %s WHERE entry_id = %s  "
        c.execute(command, (self.title, self.content, entry_id))
    ''' checking entries with same title '''   
    def check_entry_duplicate(self):
        command = "SELECT title FROM entries where email = %s"
        c.execute(command,(self.email,))
        value = c.fetchall()
        return value
    

db=Database()



       



  