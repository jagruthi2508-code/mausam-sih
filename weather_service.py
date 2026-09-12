import openmeteo_requests
import requests_cache
from retry_requests import retry


# Create a cache so repeated requests don't unnecessarily hit the API
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
        "hourly": [
            "temperature_2m",
            "precipitation",
            "relative_humidity_2m",
            "wind_speed_10m",
            "uv_index"
        ],
        "forecast_days": 1
    }

    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()

    temperature = hourly.Variables(0).ValuesAsNumpy()
    precipitation = hourly.Variables(1).ValuesAsNumpy()
    humidity = hourly.Variables(2).ValuesAsNumpy()
    wind_speed = hourly.Variables(3).ValuesAsNumpy()
    uv_index = hourly.Variables(4).ValuesAsNumpy()

    return {
        "temperature": temperature.tolist(),
        "precipitation": precipitation.tolist(),
        "humidity": humidity.tolist(),
        "wind_speed": wind_speed.tolist(),
        "uv_index": uv_index.tolist()
    }