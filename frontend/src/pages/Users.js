import React, { useState } from 'react';
import axios from 'axios';

function Users({ users, onUserDeleted }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const deleteUser = async (username) => {
    if (window.confirm(`Are you sure you want to delete "${username}"?`)) {
      setLoading(true);
      try {
        const response = await axios.delete(`/api/delete-user/${username}`);
        setMessage(response.data.message);
        setMessageType('success');
        setTimeout(() => {
          onUserDeleted();
          setMessage('');
        }, 1500);
      } catch (error) {
        setMessage(error.response?.data?.message || 'Failed to delete user');
        setMessageType('error');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="page-container">
      <h2 className="page-title">👥 Registered Users</h2>

      {message && (
        <div className={`message ${messageType}`}>
          {message}
        </div>
      )}

      {users.length === 0 ? (
        <div className="message info">
          No registered users yet. <a href="#/" style={{ color: '#0c5460', textDecoration: 'underline' }}>Register a new user</a>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '2rem', fontSize: '1.1rem', color: '#666' }}>
            Total users: <strong>{users.length}</strong>
          </div>

          <div className="users-grid">
            {users.map((user) => (
              <div key={user} className="user-card">
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>👤</div>
                <h3>{user}</h3>
                <button
                  className="btn btn-danger"
                  onClick={() => deleteUser(user)}
                  disabled={loading}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
