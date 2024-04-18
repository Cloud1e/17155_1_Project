from app import app

def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    
def test_admin():
    tester = app.test_client()
    response = tester.get('/admin')
    assert response.status_code == 200
    
def test_admin():
    tester = app.test_client()
    response = tester.get('/home/')
    assert response.status_code == 200

