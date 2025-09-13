# src/weather.py
import requests
from typing import Dict
from src.config import settings

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_for_city(city: str, api_key: str | None = None, units: str = "metric") -> Dict:
    key = api_key or settings.OPENWEATHER_API_KEY
    if not key:
        raise ValueError("OPENWEATHER_API_KEY not set in env or passed to function.")
    params = {"q": city, "appid": key, "units": units}
    resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        # Provide clearer diagnostics
        try:
            detail = resp.json()
        except Exception:
            detail = {"message": resp.text}
        if resp.status_code == 401:
            raise ValueError(f"OpenWeather unauthorized (401). Check OPENWEATHER_API_KEY and account status. Details: {detail}") from e
        raise ValueError(f"OpenWeather error {resp.status_code}. Details: {detail}") from e
    return resp.json()

def summarize_weather_payload(payload: dict) -> str:
    """
    Minimal helper to summarize the weather JSON into readable text.
    The LLM can be used to produce richer natural language summary.
    """
    name = payload.get("name")
    main = payload.get("main", {})
    weather = payload.get("weather", [{}])[0].get("description", "")
    temp = main.get("temp")
    feels_like = main.get("feels_like")
    humidity = main.get("humidity")
    wind = payload.get("wind", {}).get("speed")
    return (f"Weather in {name}: {weather}. Temp: {temp}°C (feels like {feels_like}°C). "
            f"Humidity: {humidity}%. Wind: {wind} m/s.")
