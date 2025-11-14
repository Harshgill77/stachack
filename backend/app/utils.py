import joblib
import sys
import os
import pandas as pd
import requests

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.weather_api import get_weather_and_rainfall

# ------------------------------
# 📍 Location Detection Function
# ------------------------------
def get_current_location():
    """
    Automatically detects current location using IP-based geolocation.
    Returns latitude, longitude, city, and country.
    Falls back to default location if detection fails.
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
    except:
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
        
        # Silently fall back to default location
        # This is normal behavior when location APIs are rate-limited
        return 30.9, 75.8, "Ludhiana", "India"


# ------------------------------
# 🌾 Load trained model and scaler
# ------------------------------
# Use absolute paths relative to this file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(BASE_DIR, "model", "crop_recommendation_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and Scaler loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model/scaler: {e}")
    model = None
    scaler = None


# ------------------------------
# 🌾 LIVE MODE - Auto fetch weather data
# ------------------------------
def recommend_crop_live(N, P, K, ph, lat, lon, api_key, iot_sensor_data=None):
    """
    🌐 LIVE MODE: Recommends crop using live weather data from APIs
    and soil data from IoT sensors (future) or manual input.

    Args:
        N, P, K: Soil nutrients (Nitrogen, Phosphorus, Potassium)
        ph: Soil pH value
        lat, lon: GPS coordinates of location
        api_key: OpenWeather API key
        iot_sensor_data: (Optional) Dict with IoT sensor readings
                        {'N': val, 'P': val, 'K': val, 'ph': val}

    Returns:
        dict: Recommended crop + weather conditions + data source info
    """
    
    if model is None or scaler is None:
        return {"error": "Model or scaler not loaded properly."}

    # Use IoT sensor data if available, otherwise use manual soil data
    if iot_sensor_data:
        print("📡 Using IoT sensor data for soil parameters...")
        N = iot_sensor_data.get('N', N)
        P = iot_sensor_data.get('P', P)
        K = iot_sensor_data.get('K', K)
        ph = iot_sensor_data.get('ph', ph)
        soil_data_source = "IoT Sensors"
    else:
        soil_data_source = "Manual Input"

    # 1️⃣ Get live weather + rainfall data from APIs
    print("⏳ Fetching live weather data from APIs...")
    temp, humidity, rainfall = get_weather_and_rainfall(lat, lon, api_key)

    if temp is None or humidity is None:
        return {"error": "Failed to fetch weather data. Check API key or internet connection."}

    print(f"✅ Weather data: Temp={temp}°C, Humidity={humidity}%, Rainfall={rainfall}mm")

    # 2️⃣ Prepare input features for ML model
    # Order must match your training dataset columns: N, P, K, temperature, humidity, ph, rainfall
    features = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], 
                           columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

    # 3️⃣ Scale input
    try:
        scaled_features = scaler.transform(features)
    except Exception as e:
        return {"error": f"Scaling failed: {e}"}

    # 4️⃣ Predict the crop
    try:
        prediction = model.predict(scaled_features)
        recommended_crop = prediction[0]
    except Exception as e:
        return {"error": f"Model prediction failed: {e}"}

    # 5️⃣ Return final results
    result = {
        "recommended_crop": recommended_crop,
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "rainfall": round(rainfall, 2),
        "mode": "LIVE",
        "soil_data_source": soil_data_source,
        "weather_data_source": "Live APIs (OpenWeather + NASA)",
        "input_data": {
            "N": N,
            "P": P,
            "K": K,
            "ph": ph
        }
    }

    return result


# ------------------------------
# 📝 MANUAL MODE - All data manual
# ------------------------------
def recommend_crop_manual(N, P, K, temperature, humidity, ph, rainfall):
    """
    ✍️ MANUAL MODE: Recommends crop using all manually entered data.
    User provides both soil data AND weather data manually.

    Args:
        N, P, K: Soil nutrients (Nitrogen, Phosphorus, Potassium)
        temperature: Temperature in °C
        humidity: Humidity in %
        ph: Soil pH value
        rainfall: Rainfall in mm

    Returns:
        dict: Recommended crop + input data info
    """
    
    if model is None or scaler is None:
        return {"error": "Model or scaler not loaded properly."}

    print("✍️  Using manual data for all parameters...")

    # 1️⃣ Prepare input features for ML model
    features = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]], 
                           columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

    # 2️⃣ Scale input
    try:
        scaled_features = scaler.transform(features)
    except Exception as e:
        return {"error": f"Scaling failed: {e}"}

    # 3️⃣ Predict the crop
    try:
        prediction = model.predict(scaled_features)
        recommended_crop = prediction[0]
    except Exception as e:
        return {"error": f"Model prediction failed: {e}"}

    # 4️⃣ Return final results
    result = {
        "recommended_crop": recommended_crop,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "rainfall": round(rainfall, 2),
        "mode": "MANUAL",
        "soil_data_source": "Manual Input",
        "weather_data_source": "Manual Input",
        "input_data": {
            "N": N,
            "P": P,
            "K": K,
            "ph": ph
        }
    }

    return result


# ------------------------------
# 🔄 Legacy function (backward compatibility)
# ------------------------------
def recommend_crop(N, P, K, ph, lat, lon, api_key):
    """
    Legacy function - redirects to recommend_crop_live()
    Kept for backward compatibility.
    """
    return recommend_crop_live(N, P, K, ph, lat, lon, api_key)


# ------------------------------
# 🧪 Interactive Test Function
# ------------------------------
if __name__ == "__main__":
    api_key = "8f96af8e0f2466de3a56b467fd29ea79"
    
    print("\n" + "="*60)
    print("🌾 CROP RECOMMENDATION SYSTEM")
    print("="*60)
    print("\nSelect Mode:")
    print("1. 🌐 LIVE MODE - Auto-detect location & fetch weather")
    print("2. ✍️  MANUAL MODE - Enter all data manually")
    print("="*60)
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        # ========== LIVE MODE - Auto-detect location ==========
        print("\n" + "="*60)
        print("🌐 LIVE MODE - Auto Location & Weather Detection")
        print("="*60 + "\n")
        
        # Ask for permission to detect location
        print("📍 Location Detection Permission")
        print("This app needs to detect your location to fetch weather data.")
        permission = input("Allow location detection? (yes/no): ").strip().lower()
        
        if permission in ['yes', 'y']:
            print("\n⏳ Detecting your location...")
            lat, lon, city, country = get_current_location()
            print(f"✅ Location Detected: {city}, {country}")
            print(f"   Coordinates: Lat {lat}, Lon {lon}")
        else:
            print("\n❌ Location permission denied.")
            print("📍 Using default location: Ludhiana, India")
            lat, lon, city, country = 30.9, 75.8, "Ludhiana", "India"
        
        print("\n" + "-"*60)
        print("Enter Soil Data:")
        try:
            N = float(input("  Nitrogen (N): "))
            P = float(input("  Phosphorus (P): "))
            K = float(input("  Potassium (K): "))
            ph = float(input("  pH value: "))
        except ValueError:
            print("❌ Invalid input. Exiting...")
            exit(1)
        
        print("\n⏳ Fetching live weather data for your location...")
        result = recommend_crop_live(N, P, K, ph, lat, lon, api_key)
        
        print("\n" + "="*60)
        print("📋 RESULT")
        print("="*60)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n🌾 RECOMMENDED CROP: {result['recommended_crop'].upper()}")
            print(f"\n📍 Location: {city}, {country}")
            print(f"   Coordinates: Lat {lat}, Lon {lon}")
            print(f"\n📡 Mode: {result['mode']}")
            print(f"🌱 Soil Data Source: {result['soil_data_source']}")
            print(f"🌤️  Weather Data Source: {result['weather_data_source']}")
            print(f"\n📊 Weather Data (Live from APIs):")
            print(f"  • Temperature: {result['temperature']}°C")
            print(f"  • Humidity: {result['humidity']}%")
            print(f"  • Rainfall: {result['rainfall']}mm/day")
            print(f"\n🌱 Soil Data (Your Input):")
            print(f"  • Nitrogen (N): {result['input_data']['N']}")
            print(f"  • Phosphorus (P): {result['input_data']['P']}")
            print(f"  • Potassium (K): {result['input_data']['K']}")
            print(f"  • pH: {result['input_data']['ph']}")
        
        print("="*60 + "\n")
    
    elif choice == "2":
        # ========== MANUAL MODE - Take all data input ==========
        print("\n" + "="*60)
        print("✍️  MANUAL MODE - Enter All Data")
        print("="*60 + "\n")
        
        print("Enter Soil Data:")
        try:
            N = float(input("  Nitrogen (N): "))
            P = float(input("  Phosphorus (P): "))
            K = float(input("  Potassium (K): "))
            ph = float(input("  pH value: "))
        except ValueError:
            print("❌ Invalid soil data. Exiting...")
            exit(1)
        
        print("\nEnter Weather Data:")
        try:
            temperature = float(input("  Temperature (°C): "))
            humidity = float(input("  Humidity (%): "))
            rainfall = float(input("  Rainfall (mm): "))
        except ValueError:
            print("❌ Invalid weather data. Exiting...")
            exit(1)
        
        print("\n⏳ Processing...")
        result = recommend_crop_manual(N, P, K, temperature, humidity, ph, rainfall)
        
        print("\n" + "="*60)
        print("📋 RESULT")
        print("="*60)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n🌾 RECOMMENDED CROP: {result['recommended_crop'].upper()}")
            print(f"\n📝 Mode: {result['mode']}")
            print(f"🌱 Soil Data Source: {result['soil_data_source']}")
            print(f"🌤️  Weather Data Source: {result['weather_data_source']}")
            print(f"\n📊 Weather Data (Your Input):")
            print(f"  • Temperature: {result['temperature']}°C")
            print(f"  • Humidity: {result['humidity']}%")
            print(f"  • Rainfall: {result['rainfall']}mm")
            print(f"\n🌱 Soil Data (Your Input):")
            print(f"  • Nitrogen (N): {result['input_data']['N']}")
            print(f"  • Phosphorus (P): {result['input_data']['P']}")
            print(f"  • Potassium (K): {result['input_data']['K']}")
            print(f"  • pH: {result['input_data']['ph']}")
        
        print("="*60 + "\n")
    
    else:
        print("\n❌ Invalid choice! Please run again and select 1 or 2.")
        exit(1)
