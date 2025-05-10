import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App'; // Importing App.js

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Rendering App component in the 'root' div
);
