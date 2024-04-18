from app import app
import unittest

class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # def test_getHwAvailability(self):
    #     hardwareName = "HW Set1"
    #     response = self.client.post('/hwsets/getAvailability', 
    #         json = {'hardwarename': hardwareName})
    #     self.assertEqual(response.data.decode('utf-8'), "20")
        
    # def test_getHwCapacity(self):
    #     hardwareName = "HW Set1"
    #     response = self.client.post('/hwsets/getCapacity', 
    #         json = {'hardwarename': hardwareName})
    #     self.assertEqual(response.data.decode('utf-8'), "20")
        
    def test_getAllHw(self):
        response = self.client.get('/hwsets/getAll/')
        self.assertEqual(response.status_code, 200)
        
    def test_checkOut(self):
        hardwareName = "HW Set1"
        quantity = "2"
        response = self.client.post('/hwsets/checkOut/', 
            json = {'hardwarename': hardwareName,
                    "quantity": quantity})
        self.assertEqual(response.status_code, 200)
    
    def test_checkIn(self):
        hardwareName = "HW Set1"
        quantity = "2"
        response = self.client.post('/hwsets/checkIn/', 
            json = {'hardwarename': hardwareName,
                    "quantity": quantity})
        self.assertEqual(response.status_code, 200)
   