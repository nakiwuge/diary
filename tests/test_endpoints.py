import unittest
import json
from v1 import app
from tests.test_models import db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):         
        self.client = app.test_client()  
        db.create_table()
    ''' user authentication tests'''
    def test_valid_user_registration(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"the registration was successful", response.data)

    def test_empty_password_field(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please add password", response.data)
    
    def test_empty_confirm_password_field(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":""}),
            content_type='application/json'
        )
        self.assertIn(b"please add confirm password", response.data)
        print (response.data)

    def test_paswwords_donot_match(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"125"}),
            content_type='application/json'
        )
        self.assertIn(b"The passwords donot match, please try again", response.data)

    def test_empty_username_field(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please add username", response.data)
    
    def test_invalid_email_field(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please fill in a valid email adress", response.data)

    def test_missing_email_field(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please add email", response.data)

    def test_duplicate_emails(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"the email adress provided is already used", response.data)
    def test_email_not_in_database(self):
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"jon@gmail.com", "password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"The email adress provided doesnot exist, please signup", response.data)

    def test_for_wrong_password(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"1"}),
            content_type='application/json'
        )
        self.assertIn(b"wrong password or email", response.data)

    def test_for_sucessfull_login(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"you have been logged in", response.data)
    ''' tests for creating and getting entries'''
    def test_empty_title_field(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
        response = self.client.post(
            '/api/v1/entries',
            headers=dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"","content":"something"}),
            content_type='application/json' 
        )
        self.assertIn(b"please add title", response.data)
    def test_empty_content_field(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"anything","content":""}),
            content_type='application/json' 
        )
        self.assertIn(b"please add content", response.data)

    def test_for_duplicate_title(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"anything","content":"something"}),
            content_type='application/json' 
        )
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"anything","content":"something"}),
            content_type='application/json' 
        )
        self.assertIn(b"entry alredy exists", response.data)

    
    def test_for_succefully_add_entry(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"anything","content":"something"}),
            content_type='application/json' 
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"entry has been added successfully", response.data)

    def test_for_getting_entries(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({
                "entry_id":"1",
                "date":"02-18-18", 
                "title":"anything",
                "content":"something"
                }),
            content_type='application/json' 
        )
        response = self.client.get(
            '/api/v1/entries/1',
            headers= dict(Authorization='Bearer '+ token),
            content_type='application/json' 
        )
        self.assertEqual(response.status_code, 200)
    ''' tests for modifying entries'''
    def test_for_successfull_update(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.client.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({
                "entry_id":"1",
                "date":"02-18-18", 
                "title":"anything",
                "content":"something"
                }),
            content_type='application/json' 
        )
        response = self.client.put(
            '/api/v1/entries/1',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({
                "entry_id":"1",
                "date":"02-18-18", 
                "title":"any",
                "content":"something"
                }),
            content_type='application/json' 
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"the update was successfully", response.data)
      
      
    def tearDown(self):
        #pass
        db.delete_tables()
    
if __name__ == "__main__":
    unittest.main()