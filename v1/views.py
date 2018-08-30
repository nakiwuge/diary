import re
import psycopg2
from datetime import datetime ,timedelta
from v1 import app, jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import  (create_access_token, 
get_jwt_identity, jwt_required)
from v1.models import User, Entry, Reminders

now = datetime.now()

''' signup endpoint '''
@app.route('/api/v1/auth/signup' , methods=['POST'])
def register():
    ''' getting the data from the user in json form'''
    data =request.get_json()
    ''' validating signup fields'''
    if  'username' not in data: 
        return jsonify({"message":"please add username"})
    elif not re.match("[a-zA-Z]+",data['username']): 
        return jsonify({"message":"Please add a valid username"})   
    elif  'email' not in data:
        return jsonify({"message":"please add email"})   
    elif not re.match("[a-zA-Z0-9-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", data['email']):
        return jsonify({"message":"please fill in a valid email address"})
    elif  'password' not in data or data['password']=="":
        return jsonify({"message":"please add password"})
    elif not re.match(".{3,}", data['password']):
        return jsonify({"message":"The password should have atleast 3 characters"})
    elif  'confirm_password' not in data: 
        return jsonify({"message":"please add confirm password"})
    elif data['password']!=data['confirm_password']:
        return jsonify({"message":"The passwords donot match, please try again"})
   
    '''creating an instance of  the User class'''
    
    user = User(
        data['email'], 
        data['username'], 
        generate_password_hash(data['password'])
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
    if  'email' not in data:
        return jsonify({"message":"please add email"})   
    elif not re.match("[a-zA-Z0-9-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", data['email']):
        return jsonify({"message":"please fill in a valid email adress"})
    elif  'password' not in data or data['password']=="":
        return jsonify({"message":"please add password"})
    
    user = User(data['email'],None,None)
    duplicate = User(data['email'], None, None)
    find_dup = duplicate.check_duplicate()
    ''' checking if the user has ever signup with the provided email'''
    if not find_dup:
        return jsonify({"message":"The email address provided doesnot exist, please signup"})
    
    result=user.login_user()
    ''' check password '''
    compare_passwords = check_password_hash(result[2],data['password'])
    if not compare_passwords:
        return jsonify({"message":"wrong password or email"})
    ''' generating the jwt token'''
    token = create_access_token(identity=result[0] ,expires_delta=False)
    return jsonify({
        "token":token,
        "message":"you have been logged in"
    })
    
''' get entries and post entries endpoint '''
@app.route("/api/v1/entries", methods=['GET','POST'])   
@jwt_required
def entries():
    ''' setting the date to current date'''
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    ''' creating an entry'''
    if request.method == 'POST':
        '''get current user'''
        current_user = get_jwt_identity()
        ''' getting data from the user in json form'''
        data = request.get_json()
        ''' validating fields when creating entry'''
        if  'title' not in data or data['title'].strip()=="":
            return jsonify({"message":"please add title"})
        elif not re.match("[a-zA-Z]+",data['title']):
            return jsonify({"message":"please add a valid title"})
        elif 'content' not in data or data['content'].strip()=="":
            return jsonify({"message":"please add content"})
        elif not re.match("[a-zA-Z]+",data["content"]):
            return jsonify({"message":"please add a valid content"})
        ''' creating an instance of Entry '''
        post_entry = Entry(current_user,data['title'], date , data['content'])
        '''check if the entry exists'''
        duplicate = Entry(current_user, data['title'], None,None)
        find_dup = duplicate.check_entry_duplicate()
       
        for title in find_dup:
            if title[0] == data['title']:
                return jsonify({"message":"This entry already exists. Please use a different title"})
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
@app.route("/api/v1/entries/<int:entry_id>", methods=['GET', 'PUT','DELETE'])
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
    elif request.method == 'PUT':
        ''' get modified data from user with json file '''
        data=request.get_json()
        if  'title' not in data or data['title'].strip() == "":
            return jsonify({"message":"please add title"})
        elif  'content' not in data or data['content'].strip() == "":
            return jsonify({"message":"please add content"})
        get_entry=Entry(None,data['title'], None, data['content']) 
        ''' modify entry'''
        get_entry.modify_entry(entry_id)
        result2 = Entry(current_user,None,None,None).get_entry_by_id(entry_id)
        return jsonify({
            "entry":result2,
            "message":"the update was successfull"
            }), 200
    else:
        get_entry=Entry(None,None,None,None)
        get_entry.delete_entry(entry_id)
        return jsonify({
            "message":"The entry has been deleted"
            }), 200
@app.route("/api/v1/entries/<int:entry_id>/expired", methods=['GET'])
@jwt_required
def modify_before_24hrs(entry_id):
    ''' get current user '''
    current_user = get_jwt_identity()
    result = Entry(current_user,None,None,None).get_entry_by_id(entry_id)
    ''' get date from database '''
    date = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
    exp_date =  date + timedelta(hours=24)
    if now > exp_date:
       return jsonify({
           "message":"Sorry you cannot modify this entry because it's past 24 hours"
           })
    return jsonify({
        "message":"update allowed"
        }), 200

@app.route("/api/v1/user", methods=['GET'])
@jwt_required
def getUser():
    user_info ={}
    current_user = get_jwt_identity()
    if request.method == "GET":
        user = User(current_user,None,None)
        result=user.login_user()
        user_info["email"] = result[0]
        user_info["username"] = result[1]
        return jsonify({"user":user_info})

@app.route("/api/v1/entries/notify", methods=['GET', 'POST'])
@jwt_required
def reminder():
   
    current_user = get_jwt_identity()
    if request.method == "POST":
        data = request.get_json()
        try:
            datetime.strptime(data["start_date"], "%Y-%m-%d %H:%M")
            datetime.strptime(data["end_date"], "%Y-%m-%d %H:%M")
            
        except:
            return jsonify({"message":"Incorrect data format, should be YYYY-MM-DD H:M"})
        reminder = Reminders(current_user,data["title"],data['start_date'],data["end_date"])
        reminder.add_reminder()
        return jsonify({"message":"The reminder has been added"})
    else:
        all_reminders =[]
        today = now.strftime("%Y-%m-%d %H:%M")
        reminder =Reminders(current_user,None,None,None)
        results = reminder.get_reminder()
        for result in results:
            reminders = {}
            reminders["email"] = result[0]
            reminders["id"] = result[1]
            reminders["title"] = result[2]
            reminders["start_date"] = result[3]
            reminders["end_date"] = result[4]
            all_reminders.append(reminders) 
        for reminder in results:

            if reminder[3] >= today and reminder[4] > today:
                return jsonify({
                    "reminder":reminder})
            else:
                return jsonify({"message":"there are no reminders for this day"})

        
 




