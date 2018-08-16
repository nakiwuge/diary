import os
from flask import Flask
from flask_jwt_extended import  JWTManager
from flask_cors import CORS

'''creating the app'''

app = Flask(__name__)
app.config['JWT_SECRET_KEY']= 'secret'
jwt = JWTManager(app)
CORS(app)

''' importing routes '''
from v1 import views