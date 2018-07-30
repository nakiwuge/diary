
from v1 import conn,c

class User:
    def __init__(self):
        self.c=c
        self.conn=conn
        self.conn.autocommit=True
    def create_tables(self):
        command=(
         
            '''CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50),
                email       VARCHAR(50),
                password VARCHAR(50)
            )'''
            )

        self.c.execute(command)
       



  