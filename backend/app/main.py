from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import recommend_crop_live, recommend_crop_manual, get_current_location

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

API_KEY = "8f96af8e0f2466de3a56b467fd29ea79"

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Crop Recommendation API is running"})

@app.route('/api/location', methods=['GET'])
def detect_location():
    """Detect current location"""
    try:
        lat, lon, city, country = get_current_location()
        return jsonify({
            "success": True,
            "location": {
                "latitude": lat,
                "longitude": lon,
                "city": city,
                "country": country
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recommend/live', methods=['POST'])
def recommend_live():
    """
    Live mode: Auto-detect location and fetch weather
    Request body: { N, P, K, ph, useCurrentLocation, latitude?, longitude? }
    """
    try:
        data = request.json
        
        N = float(data.get('N'))
        P = float(data.get('P'))
        K = float(data.get('K'))
        ph = float(data.get('ph'))
        
        # Get location
        if data.get('useCurrentLocation', True):
            lat, lon, city, country = get_current_location()
        else:
            lat = float(data.get('latitude', 30.9))
            lon = float(data.get('longitude', 75.8))
            city = data.get('city', 'Unknown')
            country = data.get('country', 'Unknown')
        
        # Get recommendation
        result = recommend_crop_live(N, P, K, ph, lat, lon, API_KEY)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
        
        # Add location info to result
        result["location"] = {
            "city": city,
            "country": country,
            "latitude": lat,
            "longitude": lon
        }
        result["success"] = True
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recommend/manual', methods=['POST'])
def recommend_manual():
    """
    Manual mode: All data provided by user
    Request body: { N, P, K, temperature, humidity, ph, rainfall }
    """
    try:
        data = request.json
        
        N = float(data.get('N'))
        P = float(data.get('P'))
        K = float(data.get('K'))
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        ph = float(data.get('ph'))
        rainfall = float(data.get('rainfall'))
        
        # Get recommendation
        result = recommend_crop_manual(N, P, K, temperature, humidity, ph, rainfall)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
        
        result["success"] = True
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌾 CROP RECOMMENDATION API SERVER")
    print("="*60)
    print("\n📡 Server running on: http://localhost:5001")
    print("📋 API Endpoints:")
    print("  • GET  /api/health          - Health check")
    print("  • GET  /api/location        - Detect location")
    print("  • POST /api/recommend/live  - Live mode recommendation")
    print("  • POST /api/recommend/manual - Manual mode recommendation")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
