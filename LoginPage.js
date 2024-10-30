// src/components/LoginPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './LoginPage.css'; // Import CSS

const LoginPage = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });

  const [error, setError] = useState('');
  const navigate = useNavigate(); // Initialize navigate

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({ ...credentials, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Simulate login validation
    const { username, password } = credentials;

    // Replace this logic with actual validation
    if (username && password) {
      // Assuming successful login
      navigate('/video'); // Navigate to the VideoCapture page
    } else {
      setError('Please enter both username and password');
    }
  };

  return (
    <div className="login-container">
      <h1 className="project-name">Login to Your Account</h1>

      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={credentials.username}
          onChange={handleChange}
          required
          className="input-field"
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={credentials.password}
          onChange={handleChange}
          required
          className="input-field"
        />

        <button type="submit" className="login-button">
          Login
        </button>
      </form>

      {error && <p className="error-text">{error}</p>}
      <p>Don't have an account? <a href="/signup">Sign Up</a></p>
    </div>
  );
};

export default LoginPage;
