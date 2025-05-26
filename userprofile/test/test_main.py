from fastapi.testclient import TestClient
from ..main import app
import pytest



@pytest.fixture
def client():
    return TestClient(app)

def test_app_start(client):
    assert app.title == 'User Profile Application'
    res = client.get('/')
    assert res.status_code == 200