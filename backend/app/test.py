import pandas as pd
import joblib
import sys, os
import warnings
import requests

# Suppress all warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.weather_api import get_weather_and_rainfall


def get_current_location():
    """
    Automatically detects current location using IP-based geolocation.
    Returns latitude, longitude, city, and country.
    """
    try:
        # Try ipapi.co first
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        city = data.get('city', 'Unknown')
        country = data.get('country_name', 'Unknown')
        
        # If data is valid, return it
        if lat and lon:
            return lat, lon, city, country
        else:
            raise ValueError("Invalid location data received")
    except Exception as e:
        try:
            # Fallback to ip-api.com
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                lat = data.get('lat')
                lon = data.get('lon')
                city = data.get('city', 'Unknown')
                country = data.get('country', 'Unknown')
                return lat, lon, city, country
        except:
            pass
        
        print(f"⚠️  Could not detect location automatically")
        print("📍 Using default location: Ludhiana, India")
        return 30.9, 75.8, "Ludhiana", "India"


# ---------- LOAD MODEL AND SCALER ----------
model = joblib.load("model/crop_recommendation_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# ---------- USER CHOICE: MANUAL OR AUTO ----------
print("\n" + "="*50)
print("🌾 CROP RECOMMENDATION SYSTEM 🌾")
print("="*50)
print("\nHow would you like to provide weather data?")
print("1. 🌐 Auto-detect location & fetch live weather")
print("2. ✍️  Enter details manually")
print("="*50)

choice = input("\nEnter your choice (1 or 2): ").strip()

# ---------- WEATHER DATA ----------
api_key = "8f96af8e0f2466de3a56b467fd29ea79"   # <-- Replace with your key

if choice == "1":
    # AUTO-DETECT MODE
    print("\n🌍 Detecting your location...")
    lat, lon, city, country = get_current_location()
    print(f"📍 Location Detected: {city}, {country} (Lat: {lat}, Lon: {lon})")
    
    temp, humidity, rainfall = get_weather_and_rainfall(lat, lon, api_key)
    
    # Check if weather data was fetched successfully
    if temp is None or humidity is None or rainfall is None:
        print("❌ Failed to fetch weather data. Exiting...")
        sys.exit(1)
    
    print(f"🌡️  Live Weather → Temp: {temp}°C, Humidity: {humidity}%, Rainfall: {rainfall}mm")

elif choice == "2":
    # MANUAL INPUT MODE
    print("\n✍️  Please enter the following details:")
    try:
        temp = float(input("Temperature (°C): "))
        humidity = float(input("Humidity (%): "))
        rainfall = float(input("Rainfall (mm): "))
        
        print(f"\n✅ Weather Data Entered → Temp: {temp}°C, Humidity: {humidity}%, Rainfall: {rainfall}mm")
    except ValueError:
        print("❌ Invalid input! Please enter numeric values.")
        sys.exit(1)

else:
    print("❌ Invalid choice! Please run the program again and select 1 or 2.")
    sys.exit(1)

# ---------- SOIL DATA ----------
print("\n" + "="*50)
print("How would you like to provide soil data?")
print("1. 📊 Use random sample from dataset")
print("2. ✍️  Enter soil details manually")
print("="*50)

soil_choice = input("\nEnter your choice (1 or 2): ").strip()

if soil_choice == "1":
    # USE DATASET SAMPLE
    df = pd.read_csv("data/Crop_recommendation.csv")
    sample = df.sample(1).iloc[0]
    N = sample['N']
    P = sample['P']
    K = sample['K']
    ph = sample['ph']
    
    print("\n🌱 Soil Data (from sample):")
    print(f"N: {N}, P: {P}, K: {K}, pH: {ph}")

elif soil_choice == "2":
    # MANUAL INPUT FOR SOIL
    print("\n✍️  Please enter soil details:")
    try:
        N = float(input("Nitrogen (N) content: "))
        P = float(input("Phosphorus (P) content: "))
        K = float(input("Potassium (K) content: "))
        ph = float(input("pH value: "))
        
        print(f"\n✅ Soil Data Entered → N: {N}, P: {P}, K: {K}, pH: {ph}")
    except ValueError:
        print("❌ Invalid input! Please enter numeric values.")
        sys.exit(1)

else:
    print("❌ Invalid choice! Please run the program again and select 1 or 2.")
    sys.exit(1)

# ---------- COMBINE INPUTS ----------
# Create input for model (with live temp & humidity) using DataFrame with feature names
X_input = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], 
                       columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

# ---------- SCALE INPUT AND PREDICT ----------
X_scaled = scaler.transform(X_input)
predicted_crop = model.predict(X_scaled)[0]

# ---------- DISPLAY RESULTS ----------
print("\n" + "="*50)
print("📋 PREDICTION SUMMARY")
print("="*50)
print("\n📊 Input Data Used:")
print(f"  • Nitrogen (N): {N}")
print(f"  • Phosphorus (P): {P}")
print(f"  • Potassium (K): {K}")
print(f"  • Temperature: {temp}°C")
print(f"  • Humidity: {humidity}%")
print(f"  • pH: {ph}")
print(f"  • Rainfall: {rainfall}mm")
print("\n" + "="*50)
print(f"🌾 RECOMMENDED CROP: {predicted_crop.upper()}")
print("="*50 + "\n")