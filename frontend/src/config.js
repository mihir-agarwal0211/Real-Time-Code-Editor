// frontend/src/config.js

// If we are in production (Vercel), use the Render URL.
// If we are in development (Localhost), use empty string (so the proxy handles it)
// frontend/src/config.js
export const API_BASE_URL = import.meta.env.PROD 
  ? "https://real-time-code-backend-lv3i.onrender.com" 
  : "http://127.0.0.1:8000"; // Fallback for local development