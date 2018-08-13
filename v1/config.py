import os
import psycopg2

class Config:
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
 
    ''' connecting to the database'''
    conn = psycopg2.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        dbname=os.environ.get('DATABASE'),
        )
''' setting the cursor '''
