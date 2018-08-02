import re
import psycopg2
import datetime
from flask import request, jsonify
from flask_jwt_extended import  (create_access_token, 
get_jwt_identity, jwt_required)
from v1 import app,c,conn,jwt
from v1.models import CreateTables, User, Entry
now = datetime.datetime.now()

all_entries=[]

@app.route('/api/v1/auth/signup' , methods=['POST'])
def register():
    if request.method == 'POST':

        data =request.get_json()
        if  'password' not in data or data['password'].strip()=="":
            return jsonify({"message":"please add password"})
        elif  'confirm password' not in data or data['confirm password'].strip()=="":
            return jsonify({"message":"please add confirm password"})
        elif data['password']!=data['confirm password']:
            return jsonify({"message":"The passwords donot match, please try again"})
        elif  'username' not in data or data['username'].strip()=="":
            return jsonify({"message":"please add username"})
        elif  'email' not in data:
            return jsonify({"message":"please add email"})   
        elif not re.match("[^t]+@[^t]+\.[^t]+", data['email']):
            return jsonify({"message":"please fill in a valid email adress"})
        
        user = User(
            data['email'], 
            data['username'], 
            data['password']
            )
        duplicate = User(data['email'], None, None)
        find_dup = duplicate.check_duplicate()

        if find_dup:
            return jsonify({"message":"the email adress provided is already used"})

        user.add_user()
        return jsonify({"message":"the registration was successful"}),200

@app.route('/api/v1/auth/login' , methods=['POST'])
def login():
    data = request.get_json()
    user = User(data['email'],None,data['password'])
    duplicate = User(data['email'], None, None)
    find_dup = duplicate.check_duplicate()

    if not find_dup:
        return jsonify({"message":"The email adress provided doesnot exist, please signup"})

    result=user.login_user()
    if  not result:
        return jsonify({"message":"wrong password or email"})
    token = create_access_token(identity=result[0])
    return jsonify({
        "token":token,
        "message":"you have been logged in"
    })
    

@app.route("/api/v1/entries", methods=['GET','POST'])   
@jwt_required
def entries():
    date = now.strftime('%d-%m-%y')
    if request.method == 'POST':
        current_user = get_jwt_identity()
        data = request.get_json()
        if  'title' not in data or data['title'].strip()=="":
            return jsonify({"message":"please add title"})
        elif  'content' not in data or data['content'].strip()=="":
            return jsonify({"message":"please add content"})
        post_entry = Entry(current_user,data['title'], date , data['content'])
        post_entry.add_entry()
        return jsonify({"message":"entry has been added successfully"})

    else:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message':'please login'})
        get_entry=Entry(current_user,None,None,None)
        result = get_entry.get_all_entries()
        print(result)
        for entry in result:
            entries={}
            entries['id'] = entry[1]
            entries['date'] = entry[3]
            entries['title']=entry[2]
            entries['content']=entry[4]
            all_entries.append(entries)  
        return jsonify({"entries":all_entries})

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
        if  'title' not in data or data['title'].strip()=="":
            return jsonify({"message":"please add title"})
        elif  'content' not in data or data['content'].strip()=="":
            return jsonify({"message":"please add content"})
        get_entry=Entry(None,data['title'], None, data['content'])
        get_entry.modify_entry(entry_id)
        result = Entry.get_entry_by_id(entry_id)

        return jsonify({"entry":result})



        

        





        


    


