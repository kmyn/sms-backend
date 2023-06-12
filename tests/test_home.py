import pytest
from app import create_app

# Test root "/" path endpoint
@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_base_route(client):
    response = client.get("/", follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("SMS Simulation App") != -1
