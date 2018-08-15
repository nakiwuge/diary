import os
import psycopg2

class Develop:
    DEBUG = True
    conn = psycopg2.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('DBUSER'),
        password=os.environ.get('PASSWORD'),
        dbname=os.environ.get('DATABASE')
        )
class Testing:
    DEBUG = True
    conn = psycopg2.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('DBUSER'),
        password=os.environ.get('PASSWORD'),
        dbname=os.environ.get('TESTDB')
        )


 