import React, { useState, useEffect } from 'react';
import './App.css';
import WebcamCapture from './components/WebcamCapture';
import ChatInterface from './components/ChatInterface';
import EmotionDashboard from './components/EmotionDashboard';
import Disclaimer from './components/Disclaimer';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [currentEmotion, setCurrentEmotion] = useState(null);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' or 'dashboard'

  useEffect(() => {
    // Create a new session on mount
    createSession();
  }, []);

  const createSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/session/create`);
      if (response.data.success) {
        setSessionId(response.data.session_id);
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const handleEmotionDetected = (emotionData) => {
    setCurrentEmotion(emotionData);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>Mental Health Support System</h1>
        <p className="subtitle">AI-Powered Emotional Support & Monitoring</p>
      </header>

      <Disclaimer />

      <div className="main-container">
        <div className="left-panel">
          <WebcamCapture
            sessionId={sessionId}
            onEmotionDetected={handleEmotionDetected}
          />
        </div>

        <div className="right-panel">
          <div className="tab-navigation">
            <button
              className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              Chat
            </button>
            <button
              className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Emotion Dashboard
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'chat' ? (
              <ChatInterface
                sessionId={sessionId}
                currentEmotion={currentEmotion}
              />
            ) : (
              <EmotionDashboard sessionId={sessionId} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

