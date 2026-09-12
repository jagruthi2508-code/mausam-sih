import openmeteo_requests
import requests_cache
from retry_requests import retry


cache_session = requests_cache.CachedSession(
    ".cache",
    expire_after=3600
)

retry_session = retry(
    cache_session,
    retries=5,
    backoff_factor=0.2
)

openmeteo = openmeteo_requests.Client(
    session=retry_session
)


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "precipitation",
            "precipitation_probability",
            "relative_humidity_2m",
            "wind_speed_10m",
            "uv_index",
            "weather_code"
        ],
        "hourly": [
            "temperature_2m",
            "precipitation",
            "relative_humidity_2m",
            "wind_speed_10m",
            "uv_index",
            "soil_moisture_0_to_7cm"
        ],
        "daily": [
            "precipitation_sum"
        ],
        "forecast_days": 1,
        "timezone": "auto"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current weather
    current = response.Current()

    current_temperature = current.Variables(0).Value()
    current_precipitation = current.Variables(1).Value()
    current_precipitation_probability = current.Variables(2).Value()
    current_humidity = current.Variables(3).Value()
    current_wind_speed = current.Variables(4).Value()
    current_uv_index = current.Variables(5).Value()
    current_weather_code = current.Variables(6).Value()

    # Hourly weather
    hourly = response.Hourly()

    temperature = hourly.Variables(0).ValuesAsNumpy()
    precipitation = hourly.Variables(1).ValuesAsNumpy()
    humidity = hourly.Variables(2).ValuesAsNumpy()
    wind_speed = hourly.Variables(3).ValuesAsNumpy()
    uv_index = hourly.Variables(4).ValuesAsNumpy()
    soil_moisture = hourly.Variables(5).ValuesAsNumpy()

    current_soil_moisture = float(soil_moisture[0])

    # Daily weather
    daily = response.Daily()

    precipitation_sum = daily.Variables(0).ValuesAsNumpy()
    today_precipitation = float(precipitation_sum[0])

    return {
        # Hourly data
        "temperature": temperature.tolist(),
        "precipitation": precipitation.tolist(),
        "humidity": humidity.tolist(),
        "wind_speed": wind_speed.tolist(),
        "uv_index": uv_index.tolist(),
        "soil_moisture": soil_moisture.tolist(),

        # Current data
        "current_temperature": float(current_temperature),
        "current_precipitation": float(current_precipitation),
        "current_precipitation_probability": float(
            current_precipitation_probability
        ),
        "current_humidity": float(current_humidity),
        "current_wind_speed": float(current_wind_speed),
        "current_uv_index": float(current_uv_index),
        "current_weather_code": float(current_weather_code),
        "current_soil_moisture": current_soil_moisture,

        # Daily data
        "today_precipitation": today_precipitation
    }


def get_weather_alerts(
    temperature,
    precipitation_probability,
    wind_speed,
    uv_index
):
    alerts = []

    if precipitation_probability >= 60:
        alerts.append("Rain likely")

    if temperature >= 35:
        alerts.append("High temperature")

    if wind_speed >= 40:
        alerts.append("Strong winds")

    if uv_index >= 8:
        alerts.append("High UV level")

    return alerts


def get_recommendation(
    profile,
    temperature,
    precipitation_probability,
    wind_speed,
    uv_index
):
    if profile == "farmer":
        if precipitation_probability >= 60:
            return "Rain likely. Avoid irrigation."
        return "Weather looks suitable for farming."

    elif profile == "traveler":
        if precipitation_probability >= 60:
            return "Rain likely. Carry an umbrella."
        return "Weather looks suitable for travel."

    elif profile == "outdoor":
        if uv_index >= 8 or temperature >= 35:
            return "High heat or UV. Avoid long outdoor activities."

        if wind_speed >= 40:
            return "Strong winds. Outdoor activities may be risky."

        return "Weather looks suitable for outdoor activities."

    return "No specific recommendation."
