import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function ChatInterface({ sessionId, currentEmotion }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Load conversation history when session is available
    if (sessionId) {
      loadHistory();
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadHistory = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/session/${sessionId}/history`
      );
      if (response.data.success) {
        setMessages(response.data.messages || []);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Add user message to UI immediately
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat/message`, {
        message: userMessage,
        session_id: sessionId,
        current_emotion: currentEmotion?.dominant_emotion
      });

      if (response.data.success) {
        const botMessage = {
          role: 'assistant',
          content: response.data.response,
          timestamp: response.data.timestamp,
          crisis: response.data.crisis_detected || false
        };
        setMessages(prev => [...prev, botMessage]);
        
        // Show crisis alert if detected
        if (response.data.crisis_detected) {
          alert('⚠️ Crisis Detected: If you are in immediate danger, please call 911 or go to your nearest emergency room. You can also call the National Suicide Prevention Lifeline at 988 (available 24/7).');
        }
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date().toISOString(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>AI Therapy Chat</h2>
        <p className="chat-subtitle">Your safe space to express yourself</p>
      </div>

      <div className="chat-messages" ref={chatContainerRef}>
        {messages.length === 0 ? (
          <div className="welcome-message">
            <div className="welcome-icon">💬</div>
            <h3>Welcome to your support session</h3>
            <p>
              I'm here to listen and support you. Feel free to share whatever's
              on your mind. I'll respond with empathy and understanding.
            </p>
            <p className="welcome-tip">
              💡 Tip: The emotion detection can help me better understand your
              emotional state as we talk.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role} ${message.error ? 'error' : ''} ${message.crisis ? 'crisis' : ''}`}
            >
              <div className="message-content">
                {message.role === 'assistant' && (
                  <div className="message-avatar">🤖</div>
                )}
                <div className="message-bubble">
                  <p>{message.content}</p>
                  {message.timestamp && (
                    <span className="message-time">
                      {formatTime(message.timestamp)}
                    </span>
                  )}
                </div>
                {message.role === 'user' && (
                  <div className="message-avatar">👤</div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="message-avatar">🤖</div>
              <div className="message-bubble loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={sendMessage}>
        <input
          type="text"
          className="chat-input"
          placeholder="Type your message here..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          disabled={isLoading || !sessionId}
        />
        <button
          type="submit"
          className="send-button"
          disabled={isLoading || !inputMessage.trim() || !sessionId}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;

