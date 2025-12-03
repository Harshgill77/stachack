// src/config.js

// Use Render backend URL from environment variable
const API_BASE =
  import.meta.env.VITE_API_URL ||
  `${window.location.protocol}//${window.location.hostname}`;

// Ensure no trailing slash, then create /api path
export const API_URL = `${API_BASE.replace(/\/$/, "")}/api`;