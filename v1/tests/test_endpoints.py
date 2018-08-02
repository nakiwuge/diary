import unittest
import json
from v1 import app
from v1.models import db


class EntryTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        db.create_table() 

   

    def test_valid_user_registration(self):
        response = self.tester.post(
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
        print (response.data)

    def test_empty_password_field(self):
        response = self.tester.post(
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
        response = self.tester.post(
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
        response = self.tester.post(
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
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please add username", response.data)
    
    def test_ivalid_email_field(self):
        response = self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"please fill in a valid email adress", response.data)

    def test_duplicate_emails(self):
        self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.tester.post(
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
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"jon@gmail.com", "password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"The email adress provided doesnot exist, please signup", response.data)

    def test_for_wrong_password(self):
        self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"1"}),
            content_type='application/json'
        )
        self.assertIn(b"wrong password or email", response.data)

    def test_for_sucessfull_login(self):
        self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        response = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json'
        )
        self.assertIn(b"you have been logged in", response.data)
    
    def test_empty_title_field(self):
        self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
        )
        
        resp1 = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
        response = self.tester.post(
            '/api/v1/entries',
            headers=dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"","content":"something"}),
            content_type='application/json' 
        )
        self.assertIn(b"please add title", response.data)
    def test_empty_content_field(self):
        self.tester.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "username":"mim" ,
                "email":"mim@gmail.com",
                "password":"123", 
                "confirm password":"123"}),
            content_type='application/json'
            )
    
        resp1 = self.tester.post(
            '/api/v1/auth/login',
            data=json.dumps({"email":"mim@gmail.com", "password":"123"}),
            content_type='application/json', 
        )
        token=json.loads(resp1.data.decode())["token"]
       
        response = self.tester.post(
            '/api/v1/entries',
            headers= dict(Authorization='Bearer '+ token),
            data=json.dumps({"title":"anything","content":""}),
            content_type='application/json' 
        )
        self.assertIn(b"please add content", response.data)
      

    def tearDown(self):
        db.delete_tables()

if __name__ == "__main__":
    unittest.main()