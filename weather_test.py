import openmeteo_requests
import requests_cache
from retry_requests import retry


cache_session = requests_cache.CachedSession(
    '.cache',
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


url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 12.9716,
    "longitude": 77.5946,

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

print("Latitude:", response.Latitude())
print("Longitude:", response.Longitude())
print("Timezone:", response.UtcOffsetSeconds())


# Current weather
current = response.Current()

current_temperature = current.Variables(0).Value()
current_precipitation = current.Variables(1).Value()
current_precipitation_probability = current.Variables(2).Value()
current_humidity = current.Variables(3).Value()
current_wind_speed = current.Variables(4).Value()
current_uv_index = current.Variables(5).Value()
current_weather_code = current.Variables(6).Value()

print("\nCurrent weather:")
print("Temperature:", current_temperature)
print("Precipitation:", current_precipitation)
print("Precipitation probability:", current_precipitation_probability)
print("Humidity:", current_humidity)
print("Wind speed:", current_wind_speed)
print("UV index:", current_uv_index)
print("Weather code:", current_weather_code)


# Hourly weather
hourly = response.Hourly()

temperature = hourly.Variables(0).ValuesAsNumpy()
precipitation = hourly.Variables(1).ValuesAsNumpy()
humidity = hourly.Variables(2).ValuesAsNumpy()
wind_speed = hourly.Variables(3).ValuesAsNumpy()
uv_index = hourly.Variables(4).ValuesAsNumpy()
soil_moisture = hourly.Variables(5).ValuesAsNumpy()


print("\nHourly weather:")
print("Temperature:", temperature[:5])
print("Precipitation:", precipitation[:5])
print("Humidity:", humidity[:5])
print("Wind speed:", wind_speed[:5])
print("UV index:", uv_index[:5])
print("Soil moisture:", soil_moisture[:5])


# Daily precipitation
daily = response.Daily()

precipitation_sum = daily.Variables(0).ValuesAsNumpy()

today_precipitation = precipitation_sum[0]

print("\nDaily weather:")
print("Today's precipitation:", today_precipitation)
