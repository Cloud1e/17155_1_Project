from app import app
import unittest

class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        
    def test_project_detail(self):
        response = self.client.get('/project/1')
        self.assertEqual(response.status_code, 200)

    def test_createProject(self):
        projectName = "project2"
        projectID = "2"
        description = "test"
        authUsers = ["Tianyu", "user2"]
        response = self.client.post('/project/create/', 
            json = {'projectname': projectName, 
                    'projectid': projectID,
                    'description': description,
                    'authusers': authUsers})
        self.assertEqual(response.status_code, 200)
       
    def test_getAllProjects(self):
        response = self.client.get('/project/getAll/')
        self.assertEqual(response.status_code, 200)
         
    def test_getProject(self):
        projectID = "2"
        userName = "Tianyu"
        response = self.client.post('/project/get/', 
            json = {'projectid': projectID,
                    'username': userName})
        self.assertEqual(response.status_code, 200)
    
    def test_joinProject(self):
        projectID = "1"
        response = self.client.post('/project/join/', 
            json = {'projectid': projectID})
        self.assertEqual(response.status_code, 200)
                                      
    def test_getProjectInfo(self):
        projectID = "1"
        response = self.client.post('/project/getInfo/', 
            json = {'projectid': projectID})
        self.assertEqual(response.status_code, 200)
        
    def test_addUserToProject(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/addUser/', 
            json = {'projectid': projectID,
                    'addUsername': userName})
        self.assertEqual(response.status_code, 200)
        
    def test_leaveProject(self):
        projectID = "2"
        removeUsername = "user1"
        removedBy = "user2"
        response = self.client.post('/project/removeUser/', 
            json = {'projectid': projectID,
                    'removeUsername': removeUsername,
                    'removedBy': removedBy})
        self.assertEqual(response.status_code, 200)
        
    def test_leaveProjectFinal(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/removeUserFinal/', 
            json = {'projectid': projectID,
                    'removeUsername': userName})
        self.assertEqual(response.status_code, 200)
        

