import React, { useRef, useState } from 'react';
import axios from 'axios';

function Register({ onUserRegistered }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [cameraStarted, setCameraStarted] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [userName, setUserName] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' }
      });
      videoRef.current.srcObject = stream;
      setCameraStarted(true);
      setMessage('');
    } catch (error) {
      showMessage('error', 'Unable to access camera. Please check permissions.');
    }
  };

  const captureSignature = () => {
    if (!videoRef.current) return;

    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    context.drawImage(videoRef.current, 0, 0);

    setCapturedImage(canvas.toDataURL('image/png'));
    showMessage('success', 'Signature captured! Enter your name and click Register.');
  };

  const registerUser = async () => {
    if (!userName.trim()) {
      showMessage('error', 'Please enter your name.');
      return;
    }

    if (!capturedImage) {
      showMessage('error', 'Please capture a signature first.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/register', {
        name: userName,
        image: capturedImage
      });

      showMessage('success', response.data.message);
      setUserName('');
      setCapturedImage(null);
      setCameraStarted(false);
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
      setTimeout(() => onUserRegistered(), 1500);
    } catch (error) {
      showMessage('error', error.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setUserName('');
    showMessage('');
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
    setCameraStarted(false);
    setCapturedImage(null);
    setUserName('');
  };

  const showMessage = (type, text) => {
    setMessageType(type);
    setMessage(text);
  };

  return (
    <div className="page-container">
      <h2 className="page-title">📝 Register New User</h2>

      {message && (
        <div className={`message ${messageType}`}>
          {message}
        </div>
      )}

      {!cameraStarted && !capturedImage && (
        <div style={{ textAlign: 'center' }}>
          <button className="btn btn-primary" onClick={startCamera} disabled={loading}>
            Start Camera
          </button>
        </div>
      )}

      {cameraStarted && (
        <div>
          <div className="canvas-container">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              style={{
                width: '100%',
                maxWidth: '500px',
                border: '2px solid #667eea',
                borderRadius: '8px'
              }}
            />
          </div>
          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
            <button className="btn btn-primary" onClick={captureSignature} style={{ marginRight: '0.5rem' }}>
              Capture Signature
            </button>
            <button className="btn btn-danger" onClick={stopCamera}>
              Cancel
            </button>
          </div>
        </div>
      )}

      {capturedImage && (
        <div>
          <div className="canvas-container">
            <img
              src={capturedImage}
              alt="Captured Signature"
              style={{
                width: '100%',
                maxWidth: '500px',
                border: '2px solid #667eea',
                borderRadius: '8px'
              }}
            />
          </div>

          <div className="form-group" style={{ marginTop: '2rem' }}>
            <label>Name</label>
            <input
              type="text"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Enter your full name"
              disabled={loading}
            />
          </div>

          <div style={{ textAlign: 'center' }}>
            <button
              className="btn btn-primary"
              onClick={registerUser}
              disabled={loading}
              style={{ marginRight: '0.5rem' }}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
            <button
              className="btn btn-danger"
              onClick={resetCapture}
              disabled={loading}
            >
              Try Again
            </button>
          </div>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}

export default Register;
