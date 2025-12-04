// src/config.js

// Determine the backend URL
// 1. If VITE_API_URL is set in .env, use it.
// 2. If running on localhost, default to http://localhost:5001
// 3. Otherwise, assume backend is on the same host (production)
const API_BASE = import.meta.env.VITE_API_URL ||
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001'
    : `${window.location.protocol}//${window.location.hostname}`);

// Ensure no trailing slash, then create /api path
export const API_URL = `${API_BASE.replace(/\/$/, "")}/api`;