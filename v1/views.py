import re
import psycopg2
from datetime import datetime ,timedelta
from flask import request, jsonify
from flask_jwt_extended import  (create_access_token, 
get_jwt_identity, jwt_required)
from v1 import app,jwt
from v1.models import User, Entry


''' signup endpoint '''
@app.route('/api/v1/auth/signup' , methods=['POST'])
def register():
    ''' getting the data from the user in json form'''
    data =request.get_json()
    ''' validating signup fields'''
    if  'password' not in data or data['password'].strip()=="":
        return jsonify({"message":"please add password"})
    elif  'confirm_password' not in data or data['confirm_password'].strip()=="":
        return jsonify({"message":"please add confirm password"})
    elif data['password']!=data['confirm_password']:
        return jsonify({"message":"The passwords donot match, please try again"})
    elif  'username' not in data or data['username'].strip()=="":
        return jsonify({"message":"please add username"})
    elif  'email' not in data:
        return jsonify({"message":"please add email"})   
    elif not re.match("[^t]+@[^t]+\.[^t]+", data['email']):
        return jsonify({"message":"please fill in a valid email adress"})
    '''creating an instance of  the User class'''
    user = User(
        data['email'], 
        data['username'], 
        data['password']
        )
    ''' checking email dublicates'''
    duplicate = User(data['email'], None, None)
    find_dup = duplicate.check_duplicate()

    if find_dup:
        return jsonify({"message":"the email adress provided is already used"})
    ''' adding the user to the database'''
    user.add_user()
    return jsonify({"message":"the registration was successful"}),200
''' login endpoint'''
@app.route('/api/v1/auth/login' , methods=['POST'])
def login():
    ''' getting data from the user in json form'''
    data = request.get_json()
    ''' creating an instace of the user class'''
    user = User(data['email'],None,data['password'])
    duplicate = User(data['email'], None, None)
    find_dup = duplicate.check_duplicate()
    ''' checking if the user has ever signup with the provided email'''
    if not find_dup:
        return jsonify({"message":"The email adress provided doesnot exist, please signup"})
    
    result=user.login_user()
    ''' password check'''
    if  not result:
        return jsonify({"message":"wrong password or email"})
    ''' generating the jwt token'''
    token = create_access_token(identity=result[0])
    return jsonify({
        "token":token,
        "message":"you have been logged in"
    })
    
''' get entries and post entries endpoint '''
@app.route("/api/v1/entries", methods=['GET','POST'])   
@jwt_required
def entries():
    ''' setting the date to current date'''

    date = datetime.now()
    ''' creating an entry'''
    if request.method == 'POST':
        '''get current user'''
        current_user = get_jwt_identity()
        ''' getting data from the user in json form'''
        data = request.get_json()
        ''' validating fields when creating entry'''
        if  'title' not in data or data['title'].strip()=="":
            return jsonify({"message":"please add title"})
        elif 'content' not in data or data['content'].strip()=="":
            return jsonify({"message":"please add content"})
        ''' creating an instance of Entry '''
        post_entry = Entry(current_user,data['title'], date , data['content'])
        '''check if the entry exists'''
        duplicate = Entry(current_user, data['title'], None,None)
        find_dup = duplicate.check_entry_duplicate()
        print (find_dup)
        for title in find_dup:
            if title[0] == data['title']:
                return jsonify({"message":"entry alredy exists"})
        ''' create an entry '''
        result=post_entry.add_entry()
        return jsonify({
            "message":"entry has been added successfully",
            "entriey":data
            }),200
    
    else:
        ''' getting all entries of a user'''
        all_entries=[]
        ''' get current user '''
        current_user = get_jwt_identity()
        get_entry=Entry(current_user,None,None,None)
        ''' get entries of a current user '''
        result = get_entry.get_all_entries()
        if not result:
            return jsonify({"message":"there are no entries please add an entry"})
        ''' add keys to returned data '''
        for entry in result:
            entries={}
            entries['Entry_id'] = entry[1]
            entries['date'] = entry[3]
            entries['title']=entry[2]
            entries['content']=entry[4]
            all_entries.append(entries)  
        return jsonify({"entries":all_entries})
''' get entry by id and modify entry by id endpoint'''
@app.route("/api/v1/entries/<int:entry_id>", methods=['GET', 'PUT'])
@jwt_required
def modify(entry_id):
    all_entries = []
    ''' get current user '''
    current_user = get_jwt_identity()
    if request.method == 'GET':
        ''' get entry '''
        get_entry=Entry(current_user,None,None,None)
        result=get_entry.get_entry_by_id(entry_id)
        if not result or type(entry_id) != int:
             return jsonify({"message":"there are no entries with the provided id"})
        ''' add keys to returned data '''
        entries={}
        entries['Entry id'] = result[1]
        entries['date'] = result[3]
        entries['title']=result[2]
        entries['content']=result[4]
        all_entries.append(entries) 
        return jsonify({"entry":all_entries}),200
    else:
        ''' get modified data from user with json file '''
        data=request.get_json()
        
        result = Entry(current_user,None,None,None).get_entry_by_id(entry_id)
        exp_date = result.date + timedelta(hours=24)
        now = datetime.now()

        if now > exp_date:
            return jsonify({"message":"Sorry this entry cannot be edited. It is past 24 hours."})

        ''' validate modify entry fields'''
        elif  'title' not in data or data['title'].strip()=="":
            return jsonify({"message":"please add title"})
        elif  'content' not in data or data['content'].strip()=="":
            return jsonify({"message":"please add content"})
        get_entry=Entry(None,data['title'], None, data['content']) 
        ''' modify entry'''
        get_entry.modify_entry(entry_id)
        result = Entry(current_user,None,None,None).get_entry_by_id(entry_id)

        return jsonify({
            "entry":result,
            "message":"the update was successfully"
            }), 200
