from app import app
import unittest

class UserTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_createUser(self):
        username = "user4"
        password = "password"
        response = self.client.post('/createUser/', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        username = "user1"
        password = "password"
        response = self.client.post('/login/', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        
    def test_logout(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.data.decode('utf-8'), '1')
        
    

