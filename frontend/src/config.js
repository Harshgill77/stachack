// API Configuration
// Auto-detects if accessing from network or localhost

const getApiUrl = () => {
  const hostname = window.location.hostname;
  
  // If accessing via IP address (from phone), use that IP for API
  if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    return `http://${hostname}:5001/api`;
  }
  
  // If on localhost (laptop), use localhost
  return 'http://localhost:5001/api';
};

export const API_URL = getApiUrl();
