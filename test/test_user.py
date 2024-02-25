from app import app
import unittest

class UserTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_user_creation(self):
        username = "user1"
        password = "password"
        response = self.client.post('/user/create', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 201)
        self.assertIn("User " + username + " Created!", response.json['message'])

    def test_login_success(self):
        username = "user1"
        password = "password"
        response = self.client.post('/user/login', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login success!', response.json['message'])

    # def test_login_fail(self):
    #     """failed"""
    #     response = self.client.post('/login', data={'username': 'nonexistent', 'password': 'wrongpassword'})
    #     self.assertEqual(response.status_code, 401)
    #     self.assertIn('Invalid credentials', response.json['message'])
