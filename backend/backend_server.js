// backend_server.js

// Import required dependencies
const express = require('express');
const dotenv = require('dotenv');
const path = require('path');

// Initialize the app
const app = express();

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, './.env') });

// Middleware to parse JSON bodies
app.use(express.json());

// Endpoint to provide Zoho API token
app.get('/api/zoho-token', (req, res) => {
  const zohoToken = process.env.ZOHO_API_TOKEN;  // Retrieve Zoho token from .env

  if (zohoToken) {
    res.json({ access_token: zohoToken });
  } else {
    res.status(500).json({ error: 'Zoho token not found' });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

