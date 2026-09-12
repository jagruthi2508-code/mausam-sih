from fastapi import FastAPI
from weather_service import get_weather

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Mausam backend is working!"}


@app.get("/weather")
def weather(latitude: float, longitude: float):

    weather_data = get_weather(latitude, longitude)

    return weather_data