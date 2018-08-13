from flask import Flask
from flask_jwt_extended import  JWTManager
from v1.config import Config


'''creating the app'''

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
c = Config.conn.cursor()

''' importing routes '''
from v1 import views
