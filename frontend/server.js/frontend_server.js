/**
 * File: frontend_server.js
 * Description: Simple Express.js server for serving a frontend application.
 * Author: Eric Andrew Morse
 * Date: 2025-05-11
 *
 * This file creates a minimal Express server intended for use as a
 * development server or as a simple way to serve frontend files.
 * 
 * In modern React/Vite projects, this file is rarely needed, since
 * Vite provides its own dev server. If you deploy using static hosting,
 * this file is also unnecessary for production.
 */

// Import the express library
import express from 'express';

// Create an instance of an Express app
const app = express();

// Example route for testing server functionality
app.get('/', (req, res) => {
  res.send('Frontend Server Running');
});

// You can add more routes or static file serving here if needed
// For example, to serve static files from a 'dist' directory:
// app.use(express.static('dist'));

// Set the port to the environment variable PORT or default to 3000
const PORT = process.env.PORT || 3000;

// Start the server and listen on the specified port
app.listen(PORT, () => {
  console.log(`Frontend server is running on port ${PORT}`);
});

/**
 * End of frontend_server.js
 */
