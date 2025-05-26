from fastapi.testclient import TestClient
import pytest
from ..main import app
from logging import Logger

logger = Logger(__name__)

@pytest.fixture
def client():
    return TestClient(app)

def test_user_register_success(client):
    formdata = {
        'email': 'dummy@gmail.com',
        'password': 'Dummy@123',
    }

    res = client.post('/user/registration', data=formdata)
    print(res.json())
    assert res.status_code == 400

# Password validations are handled at schema level
def test_user_register_invalid_password(client):
    formdata = [
        {
            # No uppercase
            'email': 'dummy@gmail.com',
            'password': 'dummyabc@123',
            'scope': 'user-r'
        },
        {
            # No lower case
            'email': 'dummy@gmail.com',
            'password': 'DUMMYABC@123',
            'scope': 'user-r'
        },
        {
            # No special char
            'email': 'dummy@gmail.com',
            'password': 'Dummyabc123',
            'scope': 'user-r'
        },
        {
            # No digit
            'email': 'dummy@gmail.com',
            'password': 'Dummyabc@',
            'scope': 'user-r'
        },
        {
            # Min-Length constraint
            'email': 'dummy@gmail.com',
            'password': 'Dm@123',
            'scope': 'user-r'
        },
        {
            # Max-Length constraint
            'email': 'dummy@gmail.com',
            'password': 'AbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyz@123',
            'scope': 'user-r'
        },
        {
            # Scope param not provided
            'email': 'dummy@gmail.com',
            'password': 'Dummy@123',
        },
        {
            # password param not provided
            'email': 'dummy@gmail.com',
            'scope': 'user-r',
        },
        {
            # email param not provided
            'password': 'Dummy@123',
            'scope': 'user-r',
        },

    ]

    for case in formdata:
        res = client.post('/user/registration', data=case)
        assert res.status_code == 422

def test_user_login_success(client):
    formdata = {
        'email': 'dummy@gmail.com',
        'password': 'Dummy@123',
        'scope': 'user-r'
    }
    res = client.post('/user/registration', data=formdata)
    logger.info(res.json)
    assert res.status_code == 200


def test_login_route(client):
    formdata = {
        'username': 'dummy@gmail.com',
        'password': 'Dummy@1234',
        'scope': 'user-r'
    }
    res = client.post('/user/login', data=formdata)
    print(res.json())
    assert res.status_code == 200