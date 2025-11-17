import React, { useRef, useEffect, useState } from 'react';
import './WebcamCapture.css';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function WebcamCapture({ sessionId, onEmotionDetected }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [error, setError] = useState(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      stopStreaming();
    };
  }, []);

  const startStreaming = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsStreaming(true);

        // Start capturing frames every 2 seconds
        intervalRef.current = setInterval(captureAndDetect, 2000);
      }
    } catch (err) {
      setError('Unable to access camera. Please check permissions.');
      console.error('Camera access error:', err);
    }
  };

  const stopStreaming = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsStreaming(false);
  };

  const captureAndDetect = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    try {
      // Send to backend for emotion detection
      const response = await axios.post(`${API_BASE_URL}/emotion/detect`, {
        image: imageData,
        session_id: sessionId
      });

      if (response.data.success) {
        const emotionData = response.data.emotions;
        setCurrentEmotion(emotionData);
        onEmotionDetected(emotionData);
      }
    } catch (err) {
      console.error('Emotion detection error:', err);
    }
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      happy: '#4CAF50',
      sad: '#2196F3',
      angry: '#F44336',
      fear: '#9C27B0',
      surprise: '#FF9800',
      disgust: '#795548',
      neutral: '#9E9E9E'
    };
    return colors[emotion] || colors.neutral;
  };

  const getEmotionEmoji = (emotion) => {
    const emojis = {
      happy: '😊',
      sad: '😢',
      angry: '😠',
      fear: '😨',
      surprise: '😲',
      disgust: '🤢',
      neutral: '😐'
    };
    return emojis[emotion] || emojis.neutral;
  };

  return (
    <div className="webcam-container">
      <div className="webcam-header">
        <h2>Emotion Detection</h2>
        <div className="webcam-controls">
          {!isStreaming ? (
            <button className="start-button" onClick={startStreaming}>
              Start Camera
            </button>
          ) : (
            <button className="stop-button" onClick={stopStreaming}>
              Stop Camera
            </button>
          )}
        </div>
      </div>

      <div className="video-wrapper">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="video-element"
        />
        <canvas ref={canvasRef} style={{ display: 'none' }} />

        {currentEmotion && currentEmotion.faces_detected > 0 && (
          <div className="emotion-overlay">
            <div
              className="emotion-indicator"
              style={{
                backgroundColor: getEmotionColor(currentEmotion.dominant_emotion)
              }}
            >
              <span className="emotion-emoji">
                {getEmotionEmoji(currentEmotion.dominant_emotion)}
              </span>
              <span className="emotion-label">
                {currentEmotion.dominant_emotion}
              </span>
              <span className="emotion-confidence">
                {(currentEmotion.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        )}

        {!isStreaming && (
          <div className="video-placeholder">
            <div className="placeholder-icon">📷</div>
            <p>Click "Start Camera" to begin emotion detection</p>
          </div>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      {currentEmotion && currentEmotion.faces_detected > 0 && (
        <div className="emotion-details">
          <h3>Detected Emotions</h3>
          <div className="emotion-bars">
            {Object.entries(currentEmotion.emotions || {})
              .sort((a, b) => b[1] - a[1])
              .map(([emotion, confidence]) => (
                <div key={emotion} className="emotion-bar-item">
                  <div className="emotion-bar-label">
                    <span>{getEmotionEmoji(emotion)} {emotion}</span>
                    <span>{(confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="emotion-bar">
                    <div
                      className="emotion-bar-fill"
                      style={{
                        width: `${confidence * 100}%`,
                        backgroundColor: getEmotionColor(emotion)
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default WebcamCapture;

