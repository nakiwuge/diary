
import psycopg2
from validate_email import validate_email
from flask import request, jsonify
from v1 import app,c,conn
from v1.models import CreateTables, User



@app.route('/api/v1/signup' , methods=['POST'])
def register():
    if request.method == 'POST':

        data =request.get_json()
        if data['password']!=data['confirm password']:
            return jsonify("The passwords donot match, please try again")
        elif not data['username'].lower().islower():
            return jsonify("please fill in username field")
        elif not data['email'].lower().islower():
            return jsonify("please fill in email field")
        
        user = User(
            data['username'], 
            data['email'], 
            data['password']
            )
        user.add_user()
    
       
        return jsonify("the registration was successful")
@app.route('/api/v1/login' , methods=['POST'])
def login():
   pass



        


    


