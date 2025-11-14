"""
Example: How to use both LIVE and MANUAL modes
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import recommend_crop_live, recommend_crop_manual

api_key = "8f96af8e0f2466de3a56b467fd29ea79"

print("="*70)
print("🌾 CROP RECOMMENDATION SYSTEM - MODE COMPARISON")
print("="*70)

# ==================================================
# MODE 1: LIVE - Weather from APIs, Soil Manual
# ==================================================
print("\n📡 MODE 1: LIVE MODE")
print("-" * 70)
print("Weather: Fetched from APIs (OpenWeather + NASA)")
print("Soil: Manual entry or IoT sensors (future)")
print("-" * 70)

# Your location coordinates
lat, lon = 30.9, 75.8  # Ludhiana
print(f"\n📍 Location: Ludhiana (Lat: {lat}, Lon: {lon})")

# Soil data (manual or from IoT sensors)
N, P, K, ph = 90, 42, 43, 6.5
print(f"🌱 Soil Data: N={N}, P={P}, K={K}, pH={ph}")

# Get recommendation with live weather
result_live = recommend_crop_live(N, P, K, ph, lat, lon, api_key)

if "error" not in result_live:
    print(f"\n✅ Recommended Crop: {result_live['recommended_crop'].upper()}")
    print(f"   Temperature: {result_live['temperature']}°C (Live)")
    print(f"   Humidity: {result_live['humidity']}% (Live)")
    print(f"   Rainfall: {result_live['rainfall']}mm/day (7-day avg)")

# ==================================================
# MODE 2: MANUAL - All data entered manually
# ==================================================
print("\n\n✍️  MODE 2: MANUAL MODE")
print("-" * 70)
print("Weather: Manual entry")
print("Soil: Manual entry")
print("-" * 70)

# All data entered manually (e.g., from dataset or user input)
N, P, K = 90, 42, 43
temperature, humidity = 20.8, 82.0
ph, rainfall = 6.5, 202.9

print(f"\n🌱 Soil: N={N}, P={P}, K={K}, pH={ph}")
print(f"🌤️  Weather: Temp={temperature}°C, Humidity={humidity}%, Rainfall={rainfall}mm")

# Get recommendation with manual data
result_manual = recommend_crop_manual(N, P, K, temperature, humidity, ph, rainfall)

if "error" not in result_manual:
    print(f"\n✅ Recommended Crop: {result_manual['recommended_crop'].upper()}")
    print(f"   Temperature: {result_manual['temperature']}°C (Manual)")
    print(f"   Humidity: {result_manual['humidity']}% (Manual)")
    print(f"   Rainfall: {result_manual['rainfall']}mm (Manual)")

# ==================================================
# MODE 3: LIVE with IoT Sensors (Future Scope)
# ==================================================
print("\n\n📡 MODE 3: LIVE + IoT SENSORS (Future)")
print("-" * 70)
print("Weather: Fetched from APIs")
print("Soil: From IoT sensors automatically")
print("-" * 70)

# Simulate IoT sensor readings
iot_sensor_data = {
    'N': 75,
    'P': 50,
    'K': 35,
    'ph': 7.0
}

print(f"\n📡 IoT Sensor Readings:")
print(f"   N={iot_sensor_data['N']}, P={iot_sensor_data['P']}, "
      f"K={iot_sensor_data['K']}, pH={iot_sensor_data['ph']}")
print(f"📍 Location: Auto-detected or GPS-based")

# Get recommendation with IoT sensor data
result_iot = recommend_crop_live(0, 0, 0, 0, lat, lon, api_key, 
                                 iot_sensor_data=iot_sensor_data)

if "error" not in result_iot:
    print(f"\n✅ Recommended Crop: {result_iot['recommended_crop'].upper()}")
    print(f"   Soil Data Source: {result_iot['soil_data_source']}")
    print(f"   Weather Data Source: {result_iot['weather_data_source']}")
    print(f"   Temperature: {result_iot['temperature']}°C (Live API)")
    print(f"   Humidity: {result_iot['humidity']}% (Live API)")

print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)
print("✅ LIVE MODE: Best for real-time recommendations with current weather")
print("✅ MANUAL MODE: Best for testing, historical data, or offline use")
print("✅ IoT MODE: Future scope - fully automated sensor-based recommendations")
print("="*70 + "\n")
