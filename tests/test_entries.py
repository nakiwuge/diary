import unittest
import json
from v1.models import db
from tests.test_data import (signup, login, postEntries, 
    getEntries, modifyEntry,getOneEntry,deleteEntry)

class FlaskTestCase(unittest.TestCase):

    def setUp(self): 
        db.create_table()
        signup("mim","mim@gmail.com","123","123") 
        self.res = login("mim@gmail.com", "123") 
        self.token = json.loads(self.res.data.decode())["token"]  
        
    def tearDown(self):
        db.delete_tables()
    
    ''' tests for creating and getting entries'''
    def test_missing_title(self): 
        response = postEntries(None,"something",self.token)
        self.assertIn(b"please add title", response.data)

    def test_invalid_title(self): 
        response = postEntries("3?","something",self.token)
        self.assertIn(b"please add a valid title", response.data)

    def test_missing_content(self):
        response = postEntries("party",None,self.token)
        self.assertIn(b"please add content", response.data)

    def test_missing_content(self):
        response = postEntries("party",None,self.token)
        self.assertIn(b"please add content", response.data)

    def test_invalid_content(self):
        response = postEntries("party",";'23",self.token)
        self.assertIn(b"please add a valid content", response.data)

    def test_for_duplicate_title(self):
        postEntries("party","something",self.token)
        response = postEntries("party","something else",self.token)
        self.assertIn(b"This entry already exists. Please use a different title", response.data)

    def test_for_succefully_add_entry(self):
        response = postEntries("party","something",self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"entry has been added successfully", response.data)

    def test_for_getting_entries(self):
        postEntries("party","something",self.token)
        response = getEntries(self.token)
        self.assertEqual(response.status_code, 200)

    def test_for_getting_entry_by_id(self):
        postEntries("party","something",self.token)
        response = getOneEntry(self.token)
        self.assertEqual(response.status_code, 200)

    ''' tests for modifying entries'''
    def test_for_successfull_update(self):
        postEntries("party","something",self.token)
        response = modifyEntry("party two", "samething",self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"the update was successfull", response.data)

    def test_for_delete(self):
        postEntries("party","something",self.token)
        response = deleteEntry(self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The entry has been deleted", response.data)
         
if __name__ == "__main__":
    unittest.main()