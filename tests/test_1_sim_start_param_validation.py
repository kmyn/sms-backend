import pytest
import json
from app import create_app

# Test various parameter for starting the simulation job

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


# Missing failurePct
def test_sim_start_1(client):
    headers = {
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    param = {
        "numMessages": 120,
        "numSenders": 4
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
    assert out["status"].find("INVALID") != -1


# Invalid failurePct
def test_sim_start_2(client):
    headers = {
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    param = {
        "numMessages": 1200,
        "failurePct": "a",
        "numSenders": 4
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
    assert out["status"].find("INVALID") != -1


# Invalid numSenders
def test_sim_start_3(client):
    headers = {
        'Content-type':'application/json',
        'Accept':'application/json'
    }
    param = {
        "numMessages": 1200,
        "failurePct": 10.2,
        "numSenders": 4.5
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
    assert out["status"].find("INVALID") != -1

