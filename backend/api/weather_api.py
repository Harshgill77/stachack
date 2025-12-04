import requests
import datetime

# -------------------------------
# 🌡️ 1. OPENWEATHER API (Temp + Humidity)
# -------------------------------
def get_weather(lat, lon, api_key):
    """
    Fetches real-time temperature and humidity from OpenWeather API.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        if res.get('cod') != 200:
            print(f"OpenWeather Error: {res.get('message', 'Unknown error')}")
            return None, None

        temp = res['main']['temp']
        humidity = res['main']['humidity']
        return temp, humidity

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None


# -------------------------------
# 🌧️ 2. NASA POWER API (Rainfall)
# -------------------------------
def get_nasa_rainfall(lat, lon, days=30):
    """
    Fetches average daily rainfall (in mm/day) for the past 'days' (default 30)
    using NASA POWER API (no API key required).
    """
    try:
        # Use a 5-day lag to ensure data availability (NASA POWER has a delay)
        end_date = datetime.datetime.now().date() - datetime.timedelta(days=5)
        start_date = end_date - datetime.timedelta(days=days)

        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=PRECTOTCORR&community=AG&"
            f"start={start_date.strftime('%Y%m%d')}&end={end_date.strftime('%Y%m%d')}&"
            f"latitude={lat}&longitude={lon}&format=JSON"
        )

        res = requests.get(url, timeout=10).json()

        # Navigate to the rainfall data
        values = res['properties']['parameter']['PRECTOTCORR']
        if not values:
            return 0.0

        # Filter out invalid/missing values (NASA uses -999 for missing data)
        valid_values = [v for v in values.values() if v >= 0]
        
        if not valid_values:
            return 0.0
        
        # Calculate average rainfall
        avg_rainfall = sum(valid_values) / len(valid_values)
        return round(avg_rainfall, 2)

    except Exception as e:
        print(f"Error fetching NASA rainfall: {e}")
        return 0.0


# -------------------------------
# 🌍 3. COMBINED FUNCTION
# -------------------------------
def get_weather_and_rainfall(lat, lon, api_key, days=30):
    """
    Combines OpenWeather (for temp & humidity)
    and NASA POWER (for rainfall) into one call.
    Returns: temp, humidity, rainfall
    """
    temp, humidity = get_weather(lat, lon, api_key)
    rainfall = get_nasa_rainfall(lat, lon, days)

    return temp, humidity, rainfall