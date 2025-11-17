import React, { useState, useEffect } from 'react';
import './EmotionDashboard.css';
import axios from 'axios';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const EMOTION_COLORS = {
  happy: '#4CAF50',
  sad: '#2196F3',
  angry: '#F44336',
  fear: '#9C27B0',
  surprise: '#FF9800',
  disgust: '#795548',
  neutral: '#9E9E9E'
};

function EmotionDashboard({ sessionId }) {
  const [emotionHistory, setEmotionHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('all'); // 'hour', 'day', 'week', 'all'

  useEffect(() => {
    if (sessionId) {
      loadData();
      // Refresh data every 5 seconds
      const interval = setInterval(loadData, 5000);
      return () => clearInterval(interval);
    }
  }, [sessionId, timeRange]);

  const loadData = async () => {
    if (!sessionId) return;

    try {
      setLoading(true);
      const [emotionsResponse, statsResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/session/${sessionId}/emotions?limit=100`),
        axios.get(`${API_BASE_URL}/session/${sessionId}/stats`)
      ]);

      if (emotionsResponse.data.success) {
        let emotions = emotionsResponse.data.emotions || [];
        
        // Filter by time range
        if (timeRange !== 'all') {
          const now = new Date();
          const cutoff = new Date();
          
          switch (timeRange) {
            case 'hour':
              cutoff.setHours(now.getHours() - 1);
              break;
            case 'day':
              cutoff.setDate(now.getDate() - 1);
              break;
            case 'week':
              cutoff.setDate(now.getDate() - 7);
              break;
          }
          
          emotions = emotions.filter(e => new Date(e.timestamp) >= cutoff);
        }
        
        setEmotionHistory(emotions.reverse()); // Reverse to show chronological order
      }

      if (statsResponse.data.success) {
        setStats(statsResponse.data.stats);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const prepareLineChartData = () => {
    return emotionHistory.map((emotion, index) => ({
      time: new Date(emotion.timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      }),
      index: index,
      happy: emotion.emotions?.happy || 0,
      sad: emotion.emotions?.sad || 0,
      angry: emotion.emotions?.angry || 0,
      fear: emotion.emotions?.fear || 0,
      surprise: emotion.emotions?.surprise || 0,
      neutral: emotion.emotions?.neutral || 0
    }));
  };

  const prepareBarChartData = () => {
    if (!stats || !stats.emotion_distribution) return [];

    return Object.entries(stats.emotion_distribution).map(([emotion, data]) => ({
      emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
      count: data.count,
      avgConfidence: (data.avg_confidence * 100).toFixed(1)
    }));
  };

  const preparePieChartData = () => {
    if (!stats || !stats.emotion_distribution) return [];

    return Object.entries(stats.emotion_distribution).map(([emotion, data]) => ({
      name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
      value: data.count,
      color: EMOTION_COLORS[emotion] || EMOTION_COLORS.neutral
    }));
  };

  if (loading && emotionHistory.length === 0) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading emotion data...</p>
      </div>
    );
  }

  if (emotionHistory.length === 0) {
    return (
      <div className="dashboard-empty">
        <div className="empty-icon">📊</div>
        <h3>No emotion data yet</h3>
        <p>Start your camera to begin tracking emotions over time.</p>
      </div>
    );
  }

  const lineData = prepareLineChartData();
  const barData = prepareBarChartData();
  const pieData = preparePieChartData();

  return (
    <div className="emotion-dashboard">
      <div className="dashboard-header">
        <h2>Emotion Analytics</h2>
        <div className="time-range-selector">
          <button
            className={timeRange === 'hour' ? 'active' : ''}
            onClick={() => setTimeRange('hour')}
          >
            Last Hour
          </button>
          <button
            className={timeRange === 'day' ? 'active' : ''}
            onClick={() => setTimeRange('day')}
          >
            Last Day
          </button>
          <button
            className={timeRange === 'week' ? 'active' : ''}
            onClick={() => setTimeRange('week')}
          >
            Last Week
          </button>
          <button
            className={timeRange === 'all' ? 'active' : ''}
            onClick={() => setTimeRange('all')}
          >
            All Time
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="stats-cards">
          <div className="stat-card">
            <div className="stat-label">Total Detections</div>
            <div className="stat-value">{emotionHistory.length}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Session Duration</div>
            <div className="stat-value">
              {stats?.created_at
                ? `${Math.round(
                    (new Date() - new Date(stats.created_at)) / 60000
                  )} min`
                : 'N/A'}
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Messages Exchanged</div>
            <div className="stat-value">{stats?.message_count || 0}</div>
          </div>
        </div>

        <div className="chart-section">
          <h3>Emotion Trends Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="happy"
                stroke={EMOTION_COLORS.happy}
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="sad"
                stroke={EMOTION_COLORS.sad}
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="angry"
                stroke={EMOTION_COLORS.angry}
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="fear"
                stroke={EMOTION_COLORS.fear}
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="neutral"
                stroke={EMOTION_COLORS.neutral}
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="charts-row">
          <div className="chart-section">
            <h3>Emotion Distribution</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="emotion" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-section">
            <h3>Emotion Breakdown</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmotionDashboard;

