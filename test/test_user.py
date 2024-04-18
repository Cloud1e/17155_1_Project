# from app import app
# import unittest

# class UserTest(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()
#         self.client.testing = True

#     def test_createUser(self):
#         username = "user2"
#         password = "password"
#         response = self.client.post('/createUser', json={'username': username, 'password': password})
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("User " + username + " Created!", response.json['message'])
