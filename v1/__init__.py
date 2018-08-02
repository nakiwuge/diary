from flask import Flask
from flask_jwt_extended import  JWTManager
import psycopg2

'''creating the app'''
app = Flask(__name__)
''' setting secret key '''
app.config['JWT_SECRET_KEY']="secret"
jwt=JWTManager(app)
''' connecting to the database'''
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="miriam",
    dbname="mydiary",
    )
''' setting the cursor '''
c = conn.cursor()



''' importing routes '''
from v1 import views