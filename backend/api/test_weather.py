import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.weather_api import get_weather_and_rainfall

print("="*60)
print("🌡️  TESTING WEATHER API")
print("="*60)

# Use the actual API key from the project
api_key = "8f96af8e0f2466de3a56b467fd29ea79"
lat, lon = 30.9, 75.8  # Ludhiana

print(f"\n📍 Testing location: Ludhiana (Lat: {lat}, Lon: {lon})")
print("\n⏳ Fetching data from APIs...")

try:
    temp, humidity, rainfall = get_weather_and_rainfall(lat, lon, api_key)
    
    print("\n" + "="*60)
    print("✅ API RESPONSE:")
    print("="*60)
    print(f"🌡️  Temperature: {temp} °C")
    print(f"💧 Humidity: {humidity} %")
    print(f"🌧️  Rainfall (NASA 7-day avg): {rainfall} mm/day")
    print("="*60)
    
    if temp and humidity and rainfall is not None:
        print("\n✅ All APIs working correctly!")
    else:
        print("\n⚠️  Some data is missing!")
        if temp is None:
            print("  ❌ Temperature data not available")
        if humidity is None:
            print("  ❌ Humidity data not available")
        if rainfall is None:
            print("  ❌ Rainfall data not available")
            
except Exception as e:
    print(f"\n❌ Error testing APIs: {e}")
    import traceback
    traceback.print_exc()