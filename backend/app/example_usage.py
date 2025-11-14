"""
Example: How to use the recommend_crop() function from utils.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import recommend_crop

# Example 1: Recommend crop for Ludhiana
print("="*60)
print("EXAMPLE 1: Rice conditions")
print("="*60)

api_key = "8f96af8e0f2466de3a56b467fd29ea79"
lat, lon = 30.9, 75.8  # Ludhiana

# Rice-friendly soil
result = recommend_crop(
    N=90,
    P=42,
    K=43,
    ph=6.5,
    lat=lat,
    lon=lon,
    api_key=api_key
)

if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"\n🌾 Recommended: {result['recommended_crop']}")
    print(f"🌡️  Temperature: {result['temperature']}°C")
    print(f"�� Humidity: {result['humidity']}%")
    print(f"🌧️  Rainfall: {result['rainfall']}mm/day")

print("\n" + "="*60)
print("EXAMPLE 2: Different location (using your GPS)")
print("="*60)

# You can use any location's GPS coordinates
result2 = recommend_crop(
    N=20,
    P=125,
    K=200,
    ph=6.0,
    lat=28.6139,  # Delhi
    lon=77.2090,
    api_key=api_key
)

if "error" in result2:
    print(f"Error: {result2['error']}")
else:
    print(f"\n🌾 Recommended: {result2['recommended_crop']}")
    print(f"🌡️  Temperature: {result2['temperature']}°C")
    print(f"💧 Humidity: {result2['humidity']}%")
    print(f"🌧️  Rainfall: {result2['rainfall']}mm/day")

print("\n" + "="*60)
