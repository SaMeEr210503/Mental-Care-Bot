# Project Structure

```
mental-health-support-system/
│
├── backend/                          # Flask backend application
│   ├── app.py                       # Main Flask application with API endpoints
│   ├── emotion_detector.py          # Emotion detection using OpenCV and FER
│   ├── chatbot.py                   # Therapeutic chatbot with GPT integration
│   ├── database.py                  # Database handler (MongoDB/SQLite)
│   └── uploads/                     # Temporary file storage (created at runtime)
│
├── frontend/                         # React frontend application
│   ├── public/
│   │   └── index.html               # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── WebcamCapture.js     # Webcam feed and emotion detection UI
│   │   │   ├── WebcamCapture.css
│   │   │   ├── ChatInterface.js     # Chat UI component
│   │   │   ├── ChatInterface.css
│   │   │   ├── EmotionDashboard.js  # Analytics dashboard
│   │   │   ├── EmotionDashboard.css
│   │   │   ├── Disclaimer.js        # Mental health disclaimer
│   │   │   └── Disclaimer.css
│   │   ├── App.js                   # Main React component
│   │   ├── App.css                  # Main app styles
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   ├── package.json                 # Node.js dependencies
│   └── build/                       # Production build (created after npm build)
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── CHAT_EXAMPLES.md                 # Example chat sessions
├── PROJECT_STRUCTURE.md             # This file
├── .gitignore                       # Git ignore rules
├── env.example                      # Environment variables template
└── mental_health.db                 # SQLite database (created at runtime)
```

## Component Descriptions

### Backend Components

#### app.py
- Main Flask application
- REST API endpoints for:
  - Session management
  - Emotion detection
  - Chat messaging
  - Data retrieval
- CORS configuration
- Static file serving for production

#### emotion_detector.py
- Face detection using OpenCV Haar Cascades
- Emotion recognition using FER library
- Fallback emotion estimation when FER unavailable
- Returns emotion probabilities and confidence scores

#### chatbot.py
- Therapeutic response generation
- OpenAI GPT integration (optional)
- Rule-based fallback responses
- Sentiment analysis
- Emotional context integration

#### database.py
- Database abstraction layer
- Supports MongoDB and SQLite
- Session, message, and emotion logging
- Statistics and history retrieval

### Frontend Components

#### WebcamCapture
- WebRTC camera access
- Real-time frame capture
- Emotion visualization overlay
- Emotion probability bars

#### ChatInterface
- Message input and display
- Conversation history
- Loading states
- Timestamp formatting

#### EmotionDashboard
- Line charts for emotion trends
- Bar charts for emotion distribution
- Pie charts for emotion breakdown
- Time range filtering
- Session statistics

#### Disclaimer
- Mental health safety notice
- Dismissible banner
- Local storage persistence

## Data Flow

1. **Emotion Detection Flow**:
   - User enables camera → WebcamCapture component
   - Frames captured every 2 seconds
   - Base64 encoded image sent to `/api/emotion/detect`
   - Backend processes with emotion_detector.py
   - Results stored in database
   - UI updates with detected emotions

2. **Chat Flow**:
   - User types message → ChatInterface component
   - Message sent to `/api/chat/message` with current emotion context
   - Backend chatbot.py generates therapeutic response
   - Response uses conversation history and emotion data
   - Message and response stored in database
   - UI updates with new messages

3. **Dashboard Flow**:
   - User switches to dashboard tab
   - EmotionDashboard requests data from `/api/session/<id>/emotions`
   - Statistics requested from `/api/session/<id>/stats`
   - Data visualized with Recharts
   - Auto-refreshes every 5 seconds

## Database Schema

### Sessions
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Messages
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP
);
```

### Emotions
```sql
CREATE TABLE emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    dominant_emotion TEXT,
    emotions TEXT,  -- JSON string
    confidence REAL,
    faces_detected INTEGER,
    timestamp TIMESTAMP
);
```

## API Endpoints

### Health
- `GET /api/health` - Server health check

### Sessions
- `POST /api/session/create` - Create new session
- `GET /api/session/<id>/history` - Get conversation history
- `GET /api/session/<id>/emotions` - Get emotion history
- `GET /api/session/<id>/stats` - Get session statistics

### Emotion Detection
- `POST /api/emotion/detect` - Detect emotions from image

### Chat
- `POST /api/chat/message` - Send message and get response

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for GPT responses (optional)
- `MONGODB_URI` - MongoDB connection string (optional, defaults to SQLite)
- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_DEBUG` - Enable Flask debug mode

## Development Workflow

1. **Backend Development**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r ../requirements.txt
   python app.py
   ```

2. **Frontend Development**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Production Build**:
   ```bash
   cd frontend
   npm run build
   # Backend will serve from frontend/build
   ```

## Dependencies

### Python (requirements.txt)
- Flask: Web framework
- flask-cors: CORS support
- flask-socketio: WebSocket support
- opencv-python: Computer vision
- numpy: Numerical operations
- fer: Facial expression recognition
- openai: GPT API (optional)
- pymongo: MongoDB driver (optional)

### Node.js (package.json)
- react: UI framework
- react-dom: React DOM rendering
- axios: HTTP client
- recharts: Data visualization
- socket.io-client: WebSocket client

