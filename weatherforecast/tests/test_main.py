from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_weather_success():
    response = client.post("/weather", json={"city": "Moscow"})
    assert response.status_code == 200
    rs_json = response.json()
    assert "Moscow" in rs_json.get("City")
    assert "Current_weather" in rs_json
    assert "Current_weather_units" in rs_json

def test_weather_success_full():
    response = client.post("/weather", json={"city": "Moscow, Russia, 55.75222, 37.61556"})
    assert response.status_code == 200
    rs_json = response.json()
    assert "Moscow" in rs_json.get("City")
    assert "Current_weather" in rs_json
    assert "Current_weather_units" in rs_json

def test_weather_empty():
    response = client.post("/weather", json={"city": ""})

    assert response.status_code == 400
