from app import app
import unittest

class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_createProject(self):
        projectName = "project2"
        projectID = "2"
        description = "test"
        authUsers = ["Tianyu", "user2"]
        response = self.client.post('/project/create', 
            json = {'projectname': projectName, 
                    'projectid': projectID,
                    'description': description,
                    'authusers': authUsers})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Project " + projectName + " Added With ID: " + projectID + "!", response.json['message'])
        
    def test_getProject(self):
        projectID = "2"
        userName = "Tianyu"
        response = self.client.post('/project/get', 
            json = {'projectid': projectID,
                    'username': userName})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Project Accessed!", response.json['message'])
        
    def test_getProjectByID(self):
        projectID = "2"
        response = self.client.post('/project/getByID', 
            json = {'projectid': projectID})
        self.assertEqual(response.status_code, 201)
        self.assertIn("project2", response.json['projectname'])
        
    def test_addUserToProject(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/addUser', 
            json = {'projectid': projectID,
                    'username': userName})
        #self.assertEqual(response.status_code, 201)
        self.assertIn("Successfully added " + userName + " to " + projectID + "!", response.json['message'])
        
    def test_leaveProject(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/removeUser', 
            json = {'projectid': projectID,
                    'username': userName})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Successfully removed " + userName + " from " + projectID + "!", response.json['message'])
        

