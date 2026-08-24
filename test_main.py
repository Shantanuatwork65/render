from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Test home APi

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

#Test items API

def test_read_item():
    response = client.get("/items?a=5&b=10")
    assert response.status_code == 200
    assert response.json() == {"a": 5, "b": 10, "sum": 15}