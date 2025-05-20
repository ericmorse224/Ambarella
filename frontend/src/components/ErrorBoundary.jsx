/**
 * ErrorBoundary.jsx
 * 
 * Description:
 *   A React error boundary component that catches JavaScript errors anywhere in its child component tree,
 *   logs those errors, and displays a fallback UI instead of the component tree that crashed.
 * 
 * Author: Eric Morse
 * Date: May 11th, 2025
 */

import React from 'react';

/**
 * ErrorBoundary
 * 
 * A class component that implements the React error boundary pattern.
 * 
 * Usage:
 *   Wrap this component around any part of your app that you want to provide error protection for.
 *   If a child throws an error, ErrorBoundary will render a fallback error UI.
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
      super(props);
    // Initialize state to track if an error has occurred and to store the error object.
    this.state = { hasError: false, error: null };
  }

  /**
   * Invoked after an error has been thrown by a descendant component.
   * Used to update state so the next render shows the fallback UI.
   * @param {Error} error - The error thrown by a child component.
   * @returns {Object} New state with error details.
   */
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  /**
   * Invoked after an error has been thrown by a descendant component.
   * Useful for logging error details.
   * @param {Error} error - The error thrown.
   * @param {Object} errorInfo - Additional info about the error.
   */
  componentDidCatch(error, errorInfo) {
      console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  /**
   * Renders the fallback UI if an error has been caught, otherwise renders children.
   * @returns {JSX.Element}
   */
  render() {
      if (this.state.hasError) {
      // Render a user-friendly error message.
      return (
        <div role="alert" className="bg-red-100 text-red-800 p-4 rounded">
          Critical error: {this.state.error?.message || 'Unknown error'}
        </div>
      );
    }
    // No error: render child components as normal.
    return this.props.children;
  }
}

export default ErrorBoundary;