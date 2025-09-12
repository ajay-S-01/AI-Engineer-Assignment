# tests/test_weather.py
import pytest
from src import weather
from types import SimpleNamespace

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_summarize_weather_payload():
    payload = {
        "name": "TestCity",
        "main": {"temp": 21, "feels_like": 20, "humidity": 50},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 3.5}
    }
    s = weather.summarize_weather_payload(payload)
    assert "TestCity" in s and "clear sky" in s

def test_get_weather_for_city_monkeypatch(monkeypatch):
    captured = {}
    def fake_get(url, params=None, timeout=10):
        captured['url'] = url
        captured['params'] = params
        return DummyResponse({"name": params['q'], "main": {}, "weather": [{}], "wind": {}}, status_code=200)
    monkeypatch.setattr("requests.get", fake_get)
    res = weather.get_weather_for_city("FakeCity", api_key="DUMMY")
    assert res["name"] == "FakeCity"
