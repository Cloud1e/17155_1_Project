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
        
    def test_createProjectTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectname'] = 'project1212'
                sess['projectid'] = '324'
                sess['description'] = 'test_coverage'
                sess['authusers'] = "user1"
            response = client.get('/project/createTry/')
            self.assertEqual(response.status_code, 201)
       
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
        
    def test_getProjectTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
                sess['username'] = "user1"
            response = client.get('/project/getTry/')
            self.assertEqual(response.status_code, 200)
    
    def test_joinProject(self):
        projectID = "1"
        response = self.client.post('/project/join/', 
            json = {'projectid': projectID})
        self.assertEqual(response.status_code, 200)
        
    def test_joinProjectTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
                sess['username'] = "sss"
            response = client.get('/project/joinTry/')
            self.assertEqual(response.status_code, 200)
                                      
    def test_getProjectInfo(self):
        projectID = "1"
        response = self.client.post('/project/getInfo/', 
            json = {'projectid': projectID})
        self.assertEqual(response.status_code, 200)
        
    def test_getProjectInfoTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
            response = client.get('/project/getInfoTry/')
            self.assertEqual(response.status_code, 200)
        
    def test_addUserToProject(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/addUser/', 
            json = {'projectid': projectID,
                    'addUsername': userName})
        self.assertEqual(response.status_code, 200)
        
    def test_addUserToProjectTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
                sess['addUserName'] = '123'
            response = client.get('/project/addUserTry/')
            self.assertEqual(response.status_code, 201)
        
    def test_leaveProject(self):
        projectID = "2"
        removeUsername = "user1"
        removedBy = "user2"
        response = self.client.post('/project/removeUser/', 
            json = {'projectid': projectID,
                    'removeUsername': removeUsername,
                    'removedBy': removedBy})
        self.assertEqual(response.status_code, 200)
        
    def test_leaveProjectTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
                sess['removeUserName'] = 'Tianyu'
                sess['removedBy'] = 'user1'
            response = client.get('/project/removeUserTry/')
            self.assertEqual(response.status_code, 200)
        
    def test_leaveProjectFinal(self):
        projectID = "2"
        userName = "user1"
        response = self.client.post('/project/removeUserFinal/', 
            json = {'projectid': projectID,
                    'removeUsername': userName})
        self.assertEqual(response.status_code, 200)
        
    def test_leaveProjectFinalTry(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['projectid'] = '321'
                sess['removeUserName'] = 'user2'
            response = client.get('/project/removeUserFinalTry/')
            self.assertEqual(response.status_code, 201)
        

