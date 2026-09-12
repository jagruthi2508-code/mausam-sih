from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather_service import get_weather, get_weather_alerts, get_recommendation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Mausam backend is working!"}


@app.get("/weather")
def weather(latitude: float, longitude: float, profile: str = "traveler"):

    weather_data = get_weather(latitude, longitude)

    # Use current weather values
    temperature = weather_data["current_temperature"]
    precipitation = weather_data["current_precipitation"]
    precipitation_probability = weather_data["current_precipitation_probability"]
    humidity = weather_data["current_humidity"]
    wind_speed = weather_data["current_wind_speed"]
    uv_index = weather_data["current_uv_index"]

    # Alerts
    alerts = get_weather_alerts(
        temperature,
        precipitation_probability,
        wind_speed,
        uv_index
    )

    # Personalized recommendation
    recommendation = get_recommendation(
        profile,
        temperature,
        precipitation_probability,
        wind_speed,
        uv_index
    )

    return {
        "temperature": temperature,
        "precipitation": precipitation,
        "precipitation_probability": precipitation_probability,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "uv_index": uv_index,
        "weather_code": weather_data["current_weather_code"],
        "soil_moisture": weather_data["current_soil_moisture"],
        "today_precipitation": weather_data["today_precipitation"],
        "alerts": alerts,
        "recommendation": recommendation
    }
