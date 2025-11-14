import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Loader, Sprout, Thermometer, Droplets, Cloud } from 'lucide-react';
import axios from 'axios';
import { API_URL } from '../config';
import './ManualMode.css';

function ManualMode({ onBack }) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/recommend/manual`, formData);

      if (response.data.success) {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get recommendation');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setResult(null);
    setFormData({
      N: '',
      P: '',
      K: '',
      temperature: '',
      humidity: '',
      ph: '',
      rainfall: ''
    });
  };

  return (
    <motion.div
      className="manual-mode"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <button className="back-btn" onClick={onBack}>
        <ArrowLeft size={20} /> Back to Mode Selection
      </button>

      {!result ? (
        <motion.div
          className="input-screen"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h2>Manual Data Entry</h2>
          <p className="form-subtitle">Enter all soil and weather parameters manually</p>

          <form onSubmit={handleSubmit} className="manual-form">
            <div className="section">
              <h3><Sprout size={20} /> Soil Parameters</h3>
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
            </div>

            <div className="section">
              <h3><Cloud size={20} /> Weather Parameters</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label>Temperature (°C)</label>
                  <input
                    type="number"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleInputChange}
                    placeholder="e.g., 20.8"
                    required
                    step="0.01"
                  />
                </div>

                <div className="form-group">
                  <label>Humidity (%)</label>
                  <input
                    type="number"
                    name="humidity"
                    value={formData.humidity}
                    onChange={handleInputChange}
                    placeholder="e.g., 82"
                    required
                    step="0.01"
                    min="0"
                    max="100"
                  />
                </div>

                <div className="form-group">
                  <label>Rainfall (mm)</label>
                  <input
                    type="number"
                    name="rainfall"
                    value={formData.rainfall}
                    onChange={handleInputChange}
                    placeholder="e.g., 202.9"
                    required
                    step="0.01"
                    min="0"
                  />
                </div>
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
              {loading ? <><Loader className="spin" size={20} /> Analyzing...</> : 'Get Recommendation'}
            </button>
          </form>
        </motion.div>
      ) : (
        <motion.div
          className="result-screen"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="result-card">
            <div className="result-icon">
              <Sprout size={48} />
            </div>
            <h2>Recommended Crop</h2>
            <div className="crop-name">{result.recommended_crop.toUpperCase()}</div>

            <div className="result-details">
              <div className="detail-section">
                <h3><Cloud size={20} /> Weather Data (Manual Input)</h3>
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
                    <span>{result.rainfall} mm</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3><Sprout size={20} /> Soil Data (Manual Input)</h3>
                <div className="soil-grid">
                  <div>N: {result.input_data.N}</div>
                  <div>P: {result.input_data.P}</div>
                  <div>K: {result.input_data.K}</div>
                  <div>pH: {result.input_data.ph}</div>
                </div>
              </div>

              <div className="mode-badge">
                Mode: {result.mode} | Data Source: {result.soil_data_source}
              </div>
            </div>

            <div className="result-actions">
              <button className="btn btn-secondary" onClick={resetForm}>
                Try Again
              </button>
              <button className="btn btn-primary" onClick={onBack}>
                Back to Modes
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

export default ManualMode;
