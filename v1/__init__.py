import psycopg2
from flask import Flask


app = Flask(__name__)


conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="miriam",
    dbname="mydiary",
    )

c =conn.cursor()

from v1 import views