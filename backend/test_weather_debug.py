import sys
import os
import requests

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.weather_api import get_weather

def test_weather_api():
    print("Testing Weather API...")
    api_key = "8f96af8e0f2466de3a56b467fd29ea79"
    lat = 30.9
    lon = 75.8
    
    print(f"Using API Key: {api_key}")
    print(f"Coordinates: {lat}, {lon}")
    
    temp, humidity = get_weather(lat, lon, api_key)
    
    if temp is not None:
        print(f"✅ Success! Temp: {temp}, Humidity: {humidity}")
    else:
        print("❌ Failed to fetch weather data.")

if __name__ == "__main__":
    test_weather_api()
