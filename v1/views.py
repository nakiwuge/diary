
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
            data['email'], 
            data['username'], 
            data['password']
            )
        user.add_user()
        return jsonify({"message":"the registration was successful"})

@app.route('/api/v1/auth/login' , methods=['POST'])
def login():
    data = request.get_json()
    user = User(data['email'],None,data['password'])
    result=user.login_user()
    print (result[0])
    if  not result:
        return jsonify({"message":"wrong password or email"})
    token = create_access_token(identity=result[0])
    return jsonify(token=token)
    #return jsonify("you have been logged in")

@app.route("/api/v1/entries", methods=['GET','POST'])   
@jwt_required
def entries():
    if request.method == 'POST':
        current_user = get_jwt_identity()
        print(current_user)
        if not current_user:
            return jsonify({'message':'please login'})
        data = request.get_json()
        post_entry = Entry(current_user,data['title'], data['date'], data['content'])
        
        post_entry.add_entry()
        return jsonify("entry has been added successfully")

    else:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message':'please login'})
        get_entry=Entry(current_user,None,None,None)
        result = get_entry.get_all_entries()
        
        return jsonify({"entries":result})

@app.route("/api/v1/entries/<int:entry_id>", methods=['GET', 'PUT'])
@jwt_required
def modify(entry_id):
    current_user = get_jwt_identity()
    if request.method == 'GET':
        if not current_user:
            return jsonify({'message':'please login'})
        get_entry=Entry.get_entry_by_id(entry_id)
        return jsonify({"entry":get_entry})

    else:
        data=request.get_json()
        if not current_user:
            return jsonify({'message':'please login'})
        
        get_entry=Entry(None,data['title'], None, data['content'])
        get_entry.modify_entry(entry_id)
        result = Entry.get_entry_by_id(entry_id)

        return jsonify({"entry":result})



        

        





        


    


