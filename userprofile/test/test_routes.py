from fastapi.testclient import TestClient
import pytest
from ..main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_change_password(client):
    formdata = {
        'email': 'dummy@gmail.com',
        'password': 'Dummy@1234',
        'confirm_password': 'Dummy@1234'
    }

    res = client.post('/user/reset-password', data=formdata)
    print(res.json())
    assert res.status_code == 200

def test_admin_user_create(client):
    res = client.get('/admin/create-admin-user')
    assert res.status_code == 405

    res2 = client.post('/admin/create-admin-user')
    assert res2.status_code == 401 # User not authenticated
    
    headers = {''}
    res3 = client.post('/admin/create-admin-user')
    assert res3