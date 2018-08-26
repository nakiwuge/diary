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

class Production:
    DEBUG = False
    conn = psycopg2.connect(
        host='ec2-54-235-160-57.compute-1.amazonaws.com',
        user='dejkpzjbrysvkp',
        password='e44398dac8f32cdafd89972d4f254f311765bdb878c1dd327ce8f1576b692403',
        dbname='df3terog2vbq3c',
        port='5432'
        )

app_config = {
     "develop": Develop,
     "testing" : Testing,
     "production": Production
 }