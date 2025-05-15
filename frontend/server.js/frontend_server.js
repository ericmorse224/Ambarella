// Example content of frontend_server.js
import express from 'express';

const app = express();

// Setup your routes, static files, etc.
app.get('/', (req, res) => {
  res.send('Frontend Server Running');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Frontend server is running on port ${PORT}`);
});

