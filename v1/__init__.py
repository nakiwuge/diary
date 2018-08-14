import os
from flask import Flask
from flask_jwt_extended import  JWTManager



'''creating the app'''

app = Flask(__name__)
app.config['JWT_SECRET_KEY']= 'secret'
jwt = JWTManager(app)


''' importing routes '''
from v1 import views