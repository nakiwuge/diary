import unittest
import json
from v1 import app

client = app.test_client() 

def signup(username,email,password,confirm_password):
    if confirm_password == None:
        return client.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "username":username,
            "email":email,
            "password":password, 
            }),
        content_type='application/json')
    elif username == None:
        return client.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "email":email,
            "password":password, 
            }),
        content_type='application/json')
    elif email == None:
        return client.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "username":username,
            "password":password, 
            }),
        content_type='application/json')
    elif password == None:
        return client.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "username":username,
            "email":email,
            }),
        content_type='application/json')
    
    return client.post(
        '/api/v1/auth/signup',
        data=json.dumps({
            "username":username,
            "email":email,
            "password":password, 
            "confirm_password":confirm_password}),
        content_type='application/json'
    )
def login(email,password):
    return client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            "email":email, 
            "password":password}),
        content_type='application/json'
    )
def postEntries(title,content,token):
    if title == None:
        return client.post(
        '/api/v1/entries',
        headers=dict(Authorization='Bearer '+ token),
        data=json.dumps({"content":content}),
        content_type='application/json' 
        )
    elif content == None:
         return client.post(
        '/api/v1/entries',
        headers=dict(Authorization='Bearer '+ token),
        data=json.dumps({"title":title}),
        content_type='application/json' 
        )
    return client.post(
        '/api/v1/entries',
        headers=dict(Authorization='Bearer '+ token),
        data=json.dumps({"title":title,"content":content}),
        content_type='application/json' 
        )
def getEntries(token):
    return client.get(
        '/api/v1/entries',
        headers=dict(Authorization='Bearer '+ token)
        )
def getOneEntry(token):
    return client.get(
        '/api/v1/entries/1',
        headers=dict(Authorization='Bearer '+ token),
        content_type='application/json' 
        )
def modifyEntry(title,content,token): 
    return client.put(
        '/api/v1/entries/1',
        headers=dict(Authorization='Bearer '+ token),
        data=json.dumps({
            "title":title,
            "content":content
            }),
        content_type='application/json' 
        )
def deleteEntry(token): 
    return client.delete(
        '/api/v1/entries/1',
        headers=dict(Authorization='Bearer '+ token),
        content_type='application/json' 
        )
    