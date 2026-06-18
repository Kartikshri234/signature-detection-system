import React, { useRef, useState } from 'react';
import axios from 'axios';

function Detect({ users }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [cameraStarted, setCameraStarted] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [result, setResult] = useState(null);
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
      setResult(null);
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
    showMessage('success', 'Signature captured! Click "Detect" to verify.');
  };

  const detectSignature = async () => {
    if (!capturedImage) {
      showMessage('error', 'Please capture a signature first.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/detect', {
        image: capturedImage
      });

      setResult(response.data);
      showMessage('', '');
    } catch (error) {
      showMessage('error', error.response?.data?.message || 'Detection failed');
    } finally {
      setLoading(false);
    }
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setResult(null);
    showMessage('');
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
    setCameraStarted(false);
    setCapturedImage(null);
    setResult(null);
  };

  const showMessage = (type, text) => {
    setMessageType(type);
    setMessage(text);
  };

  return (
    <div className="page-container">
      <h2 className="page-title">✅ Detect Signature</h2>

      {users.length === 0 && (
        <div className="message info">
          No registered users found. Please register a user first.
        </div>
      )}

      {message && (
        <div className={`message ${messageType}`}>
          {message}
        </div>
      )}

      {!cameraStarted && !capturedImage && (
        <div style={{ textAlign: 'center' }}>
          <button
            className="btn btn-primary"
            onClick={startCamera}
            disabled={loading || users.length === 0}
          >
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

      {capturedImage && !result && (
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

          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <button
              className="btn btn-primary"
              onClick={detectSignature}
              disabled={loading}
              style={{ marginRight: '0.5rem' }}
            >
              {loading ? 'Detecting...' : 'Detect'}
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

      {result && (
        <div className={`result-display ${result.result}`}>
          <div className="result-icon">
            {result.result === 'valid' ? '✅' : '❌'}
          </div>
          <div className="result-text">
            {result.message}
          </div>

          {result.result === 'valid' && (
            <div style={{ marginTop: '1rem' }}>
              <div style={{ fontSize: '1.2rem', color: '#333', marginBottom: '0.5rem' }}>
                User: <strong>{result.name}</strong>
              </div>
              <div style={{ marginTop: '1rem' }}>
                <div style={{ color: '#666', marginBottom: '0.5rem' }}>
                  Confidence: {result.confidence}%
                </div>
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{ width: `${result.confidence}%` }}
                  >
                    {result.confidence}%
                  </div>
                </div>
              </div>
            </div>
          )}

          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <button
              className="btn btn-primary"
              onClick={resetCapture}
            >
              Try Another
            </button>
          </div>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}

export default Detect;
