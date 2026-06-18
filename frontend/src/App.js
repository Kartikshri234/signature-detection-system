import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Register from './pages/Register';
import Detect from './pages/Detect';
import Users from './pages/Users';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleUserRegistered = () => {
    fetchUsers();
    setCurrentPage('home');
  };

  const handleUserDeleted = () => {
    fetchUsers();
  };

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="logo">🖊️ Signature Detection System</h1>
          <div className="nav-links">
            <button
              className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentPage('home')}
            >
              Home
            </button>
            <button
              className={`nav-btn ${currentPage === 'register' ? 'active' : ''}`}
              onClick={() => setCurrentPage('register')}
            >
              Register
            </button>
            <button
              className={`nav-btn ${currentPage === 'detect' ? 'active' : ''}`}
              onClick={() => setCurrentPage('detect')}
            >
              Detect
            </button>
            <button
              className={`nav-btn ${currentPage === 'users' ? 'active' : ''}`}
              onClick={() => setCurrentPage('users')}
            >
              Users ({users.length})
            </button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {currentPage === 'home' && (
          <div className="home-page">
            <div className="hero">
              <h2>Welcome to Signature Detection System</h2>
              <p>A modern computer vision application for real-time signature verification</p>
              <div className="features">
                <div className="feature-card">
                  <span className="feature-icon">📝</span>
                  <h3>Register</h3>
                  <p>Register your signature for authentication</p>
                </div>
                <div className="feature-card">
                  <span className="feature-icon">✅</span>
                  <h3>Detect</h3>
                  <p>Verify and validate your signature</p>
                </div>
                <div className="feature-card">
                  <span className="feature-icon">👥</span>
                  <h3>Manage</h3>
                  <p>View and manage registered users</p>
                </div>
              </div>
              <div className="quick-actions">
                <button className="btn btn-primary" onClick={() => setCurrentPage('register')}>
                  Register New User
                </button>
                <button className="btn btn-secondary" onClick={() => setCurrentPage('detect')}>
                  Detect Signature
                </button>
              </div>
            </div>
          </div>
        )}

        {currentPage === 'register' && (
          <Register onUserRegistered={handleUserRegistered} />
        )}

        {currentPage === 'detect' && (
          <Detect users={users} />
        )}

        {currentPage === 'users' && (
          <Users users={users} onUserDeleted={handleUserDeleted} />
        )}
      </main>

      <footer className="footer">
        <p>&copy; 2024 Signature Detection System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
