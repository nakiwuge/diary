import unittest
import json
from v1.models import db
from tests.test_data import signup, login

class FlaskTestCase(unittest.TestCase):

    def setUp(self):         
        db.create_table()
   
    
    ''' user authentication tests'''
    def test_for_wrong_password(self):
        signup("mim","mim@gmail.com","123","123")
        response = login("mim@gmail.com", "1")
        self.assertIn(b"wrong password or email", response.data)

    def test_valid_user_registration(self):
        response = signup("mim","mim@gmail.com","123","123")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"the registration was successful", response.data)

    def test_missing_password(self):
        response = signup("mim","mim@gmail.com",None,"123")
        self.assertIn(b"please add password", response.data)

    def test_invalid_password(self):
        response = signup("mim","mim@gmail.com","13","13")
        self.assertIn(b"The password should have atleast 3 characters", response.data)
    
    def test_missing_confirm_password(self):
        response = signup("mim","mim@gmail.com","123",None)
        self.assertIn(b"please add confirm password", response.data)

    def test_paswwords_donot_match(self):
        response = signup("mim","mim@gmail.com","123","12")
        self.assertIn(b"The passwords donot match, please try again", response.data)

    def test_missing_username(self):
        response = signup(None,"mim@gmail.com","123","123")
        self.assertIn(b"please add username", response.data)

    def test_invalid_username(self):
        response = signup(".12","mim@gmail.com","123","123")
        self.assertIn(b"Please add a valid username", response.data)
    
    def test_invalid_email(self):
        response = signup("mim","mim@gmail","123","123")
        self.assertIn(b"please fill in a valid email address", response.data)

    def test_missing_email(self):
        response = signup("mim",None,"123","123")
        self.assertIn(b"please add email", response.data)

    def test_duplicate_emails(self):
        signup("mim","mim@gmail.com","123","123")
        response = signup("mim","mim@gmail.com","123","123")
        self.assertIn(b"the email adress provided is already used", response.data)

    def test_login_unregistered_user(self):
        response = login("brian@gmail.com","123")
        self.assertIn(b"The email address provided doesnot exist, please signup", response.data)

    def test_for_sucessfull_login(self):
        signup("mim","mim@gmail.com","123","123")
        response = login("mim@gmail.com","123")
        self.assertIn(b"you have been logged in", response.data)
    
    
    def tearDown(self):
        db.delete_tables()
    
if __name__ == "__main__":
    unittest.main()