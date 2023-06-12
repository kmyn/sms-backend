import pytest
import json
from time import sleep
from app import create_app

# Validate starting simulation job and retrieving status

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


# Get status when job is not running
def test_sim_status_begin(client):
    response = client.get("/sim/status", follow_redirects=True)
    ret = response.data.decode()
    out = json.loads(ret)
    assert response.status_code == 200
    assert out["status"].find("SUCCESS") != -1
    assert out["isActive"] is False

# Start job
def test_sim_start_1(client):
    headers = {
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    param = {
        "numMessages": 120,
        "failurePct": 10,
        "numSenders": 2
    }
    response = client.post(
        "/sim/start",
        json=param,
        headers=headers
    )

    ret = response.data.decode()
    out = json.loads(ret)
    assert response.status_code == 200
    assert out["status"].find("SUCCESS") != -1


# Start job when the above job is still running
def test_sim_start_2(client):
    headers = {
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    param = {
        "numMessages": 120,
        "failurePct": 10,
        "numSenders": 5
    }
    response = client.post(
        "/sim/start",
        json=param,
        headers=headers
    )

    ret = response.data.decode()
    out = json.loads(ret)
    print (out)
    assert response.status_code == 200
    assert out["status"].find("CONFLICT") != -1


# Get job status
def test_sim_status_end(client):
    sleep(6)
    response = client.get("/sim/status", follow_redirects=True)
    ret = response.data.decode()
    out = json.loads(ret)
    assert response.status_code == 200
    assert out["status"].find("SUCCESS") != -1
    assert out["isActive"] is True
    assert out["stats"]["received"] > 0
    assert out["stats"]["errors"] >= 0
    assert out["stats"]["processed"] > 0
    assert out["stats"]["avgProcessingTime"] > 0.0




