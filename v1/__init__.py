from flask import Flask
from flask_jwt_extended import  JWTManager
import psycopg2 
import psycopg2.extras



app = Flask(__name__)
app.config['JWT_SECRET_KEY']="secret"
jwt=JWTManager(app)

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="miriam",
    dbname="mydiary",
    )

c =conn.cursor()
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

from v1 import views