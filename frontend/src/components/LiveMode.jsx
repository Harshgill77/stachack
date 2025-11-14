import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, MapPin, Loader, Sprout, Thermometer, Droplets, Cloud } from 'lucide-react';
import axios from 'axios';
import { API_URL } from '../config';
import './LiveMode.css';

function LiveMode({ onBack }) {
  const [step, setStep] = useState('permission');
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState(null);
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    ph: ''
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleLocationPermission = async (allow) => {
    if (allow) {
      setLoading(true);
      try {
        const response = await axios.get(`${API_URL}/location`);
        if (response.data.success) {
          setLocation(response.data.location);
          setStep('input');
        }
      } catch (err) {
        // Silently use default location - this is normal behavior
        console.log('Location detection not available, using default location');
        setLocation({ city: 'Ludhiana', country: 'India', latitude: 30.9, longitude: 75.8 });
        setStep('input');
      } finally {
        setLoading(false);
      }
    } else {
      setLocation({ city: 'Ludhiana', country: 'India', latitude: 30.9, longitude: 75.8 });
      setStep('input');
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/recommend/live`, {
        ...formData,
        useCurrentLocation: true
      });

      if (response.data.success) {
        setResult(response.data);
        setStep('result');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get recommendation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="live-mode"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <button className="back-btn" onClick={onBack}>
        <ArrowLeft size={20} /> Back to Mode Selection
      </button>

      {step === 'permission' && (
        <div className="permission-screen">
          <motion.div
            className="permission-card"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
          >
            <MapPin size={64} className="permission-icon" />
            <h2>Location Detection</h2>
            <p>We'll detect your location to fetch real-time weather data for accurate crop recommendations.</p>
            <p className="info-note">💡 This uses IP-based detection (no GPS required). If detection fails, we'll use a default location - everything still works perfectly!</p>
            
            <div className="permission-buttons">
              <button 
                className="btn btn-primary"
                onClick={() => handleLocationPermission(true)}
                disabled={loading}
              >
                {loading ? <><Loader className="spin" size={20} /> Detecting...</> : 'Auto-Detect Location'}
              </button>
              <button 
                className="btn btn-secondary"
                onClick={() => handleLocationPermission(false)}
              >
                Use Default Location
              </button>
            </div>
          </motion.div>
        </div>
      )}

      {step === 'input' && location && (
        <motion.div
          className="input-screen"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="location-badge">
            <MapPin size={20} />
            <span>{location.city}, {location.country}</span>
          </div>

          <h2>Enter Soil Data</h2>
          <p className="form-subtitle">Provide the following soil parameters for analysis</p>

          <form onSubmit={handleSubmit} className="soil-form">
            <div className="form-grid">
              <div className="form-group">
                <label>Nitrogen (N)</label>
                <input
                  type="number"
                  name="N"
                  value={formData.N}
                  onChange={handleInputChange}
                  placeholder="e.g., 90"
                  required
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label>Phosphorus (P)</label>
                <input
                  type="number"
                  name="P"
                  value={formData.P}
                  onChange={handleInputChange}
                  placeholder="e.g., 42"
                  required
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label>Potassium (K)</label>
                <input
                  type="number"
                  name="K"
                  value={formData.K}
                  onChange={handleInputChange}
                  placeholder="e.g., 43"
                  required
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label>pH Value</label>
                <input
                  type="number"
                  name="ph"
                  value={formData.ph}
                  onChange={handleInputChange}
                  placeholder="e.g., 6.5"
                  required
                  step="0.01"
                  min="0"
                  max="14"
                />
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
              {loading ? <><Loader className="spin" size={20} /> Analyzing...</> : 'Get Recommendation'}
            </button>
          </form>
        </motion.div>
      )}

      {step === 'result' && result && (
        <motion.div
          className="result-screen"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <motion.div
            className="result-card"
            initial={{ y: 20 }}
            animate={{ y: 0 }}
          >
            <div className="result-icon">
              <Sprout size={48} />
            </div>
            <h2>Recommended Crop</h2>
            <div className="crop-name">{result.recommended_crop.toUpperCase()}</div>

            <div className="result-details">
              <div className="detail-section">
                <h3><MapPin size={20} /> Location</h3>
                <p>{result.location.city}, {result.location.country}</p>
                <p className="coordinates">
                  Lat: {result.location.latitude.toFixed(4)}, Lon: {result.location.longitude.toFixed(4)}
                </p>
              </div>

              <div className="detail-section">
                <h3><Cloud size={20} /> Weather Data (Live)</h3>
                <div className="weather-grid">
                  <div className="weather-item">
                    <Thermometer size={18} />
                    <span>{result.temperature}°C</span>
                  </div>
                  <div className="weather-item">
                    <Droplets size={18} />
                    <span>{result.humidity}%</span>
                  </div>
                  <div className="weather-item">
                    <Cloud size={18} />
                    <span>{result.rainfall} mm/day</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3><Sprout size={20} /> Soil Data (Your Input)</h3>
                <div className="soil-grid">
                  <div>N: {result.input_data.N}</div>
                  <div>P: {result.input_data.P}</div>
                  <div>K: {result.input_data.K}</div>
                  <div>pH: {result.input_data.ph}</div>
                </div>
              </div>
            </div>

            <button className="btn btn-primary" onClick={onBack}>
              Try Another Recommendation
            </button>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  );
}

export default LiveMode;
