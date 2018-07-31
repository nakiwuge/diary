
import psycopg2
from flask_jwt_extended import  create_access_token, get_jwt_identity, jwt_required
from flask import request, jsonify
from v1 import app,c,conn,jwt
from v1.models import CreateTables, User, Entry


@app.route('/api/v1/auth/signup' , methods=['POST'])
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
        #token = create_access_token(identity=data['email'])
        #return jsonify(token=token)
        #return jsonify("the registration was successful")

@app.route('/api/v1/auth/login' , methods=['POST'])
def login():
    data = request.get_json()
    user = User(None,data['email'],data['password'])
    result=user.login_user()
    
    if  result:
        token = create_access_token(identity=result)
        return jsonify(token=token)
    else:    
        return jsonify({"msg":"wrong password or email"})
   
    #return jsonify("you have been logged in")

@app.route("/api/v1/entries", methods=['GET','POST'])   
@jwt_required
def entries():
    if request.method == 'POST':
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message':'please login'})
        data = request.get_json()
        post_entry = Entry(data['title'], data['date'], data['content'])
        post_entry.add_entry()
        return jsonify("entry has been added successfully")

    else:
        get_entry=Entry.get_all_entries()
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message':'please login'})

        return jsonify({"entries":get_entry})
        





        


    


