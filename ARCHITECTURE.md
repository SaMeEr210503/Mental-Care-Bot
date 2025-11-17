# System Architecture

## Overview

The Mental Health Support System is a full-stack application that combines real-time facial emotion recognition with an AI-powered therapeutic chatbot. The system is designed to provide empathetic, non-judgmental emotional support while monitoring users' emotional states.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Webcam     │  │     Chat     │  │  Dashboard   │     │
│  │   Capture    │  │  Interface   │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │ HTTP/WebSocket   │                  │
          │                  │                  │
┌─────────┴──────────────────┴──────────────────┴─────────────┐
│                    Flask Backend (Port 5000)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Emotion    │  │   Chatbot    │  │  Database    │     │
│  │   Detector   │  │   Module     │  │   Handler    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         │ OpenCV/FER       │ OpenAI API       │ SQLite/     │
│         │                  │ (Optional)       │ MongoDB     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Computer │      │   GPT    │      │ Database │
    │  Vision  │      │   API    │      │          │
    │  Models  │      │          │      │          │
    └──────────┘      └──────────┘      └──────────┘
```

## Component Architecture

### 1. Frontend Layer (React)

**Technology Stack:**
- React 18.2.0
- Axios for HTTP requests
- Recharts for data visualization
- WebRTC for camera access

**Key Components:**

#### WebcamCapture
- **Purpose**: Real-time video capture and emotion visualization
- **Responsibilities**:
  - Access user's webcam via WebRTC
  - Capture frames every 2 seconds
  - Send frames to backend for emotion detection
  - Display detected emotions with visual indicators
  - Show emotion probability bars

#### ChatInterface
- **Purpose**: Conversational interface for therapy sessions
- **Responsibilities**:
  - Display conversation history
  - Handle user input
  - Send messages to backend with emotional context
  - Display AI responses
  - Manage loading states

#### EmotionDashboard
- **Purpose**: Analytics and visualization of emotional patterns
- **Responsibilities**:
  - Fetch emotion history from backend
  - Display time-series charts
  - Show emotion distribution
  - Provide session statistics
  - Support time range filtering

### 2. Backend Layer (Flask)

**Technology Stack:**
- Flask 3.0.0
- Flask-CORS for cross-origin requests
- Flask-SocketIO for WebSocket support
- OpenCV for computer vision
- FER for emotion recognition

**Key Modules:**

#### app.py (Main Application)
- **Purpose**: API server and request routing
- **Endpoints**:
  - `POST /api/emotion/detect`: Process images for emotion detection
  - `POST /api/chat/message`: Handle chat messages and generate responses
  - `POST /api/session/create`: Create new therapy sessions
  - `GET /api/session/<id>/history`: Retrieve conversation history
  - `GET /api/session/<id>/emotions`: Retrieve emotion logs
  - `GET /api/session/<id>/stats`: Get session statistics

#### emotion_detector.py
- **Purpose**: Facial emotion recognition
- **Process**:
  1. Receive base64-encoded image
  2. Decode and convert to OpenCV format
  3. Detect faces using Haar Cascade
  4. Extract face regions
  5. Run emotion classification (FER or fallback)
  6. Aggregate results from multiple faces
  7. Return emotion probabilities and confidence scores

**Emotion Labels:**
- Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral

#### chatbot.py
- **Purpose**: Generate therapeutic responses
- **Process**:
  1. Analyze message sentiment
  2. Build emotional context from facial detection
  3. Retrieve conversation history
  4. Generate response (GPT or rule-based)
  5. Return empathetic, therapeutic response

**Therapeutic Techniques:**
- Reflective listening
- Validation
- Open-ended questions
- Normalization
- Empathy
- Gentle exploration

#### database.py
- **Purpose**: Data persistence and retrieval
- **Features**:
  - Supports MongoDB and SQLite
  - Session management
  - Message logging
  - Emotion logging
  - Statistics aggregation

### 3. Data Layer

**Database Options:**
1. **SQLite** (Default)
   - File-based, no setup required
   - Suitable for development and small deployments
   - Automatic schema creation

2. **MongoDB** (Optional)
   - Document-based, scalable
   - Suitable for production deployments
   - Requires MongoDB server

**Schema Design:**

```
Sessions
├── session_id (PK)
├── created_at
└── updated_at

Messages
├── id (PK)
├── session_id (FK)
├── role (user/assistant)
├── content
└── timestamp

Emotions
├── id (PK)
├── session_id (FK)
├── dominant_emotion
├── emotions (JSON)
├── confidence
├── faces_detected
└── timestamp
```

## Data Flow

### Emotion Detection Flow

```
1. User enables camera
   ↓
2. WebcamCapture captures frame every 2s
   ↓
3. Frame converted to base64
   ↓
4. POST /api/emotion/detect
   ↓
5. emotion_detector.py processes image
   ↓
6. Results stored in database
   ↓
7. Response sent to frontend
   ↓
8. UI updates with detected emotions
```

### Chat Flow

```
1. User types message
   ↓
2. Current emotion context included
   ↓
3. POST /api/chat/message
   ↓
4. chatbot.py analyzes:
   - Message sentiment
   - Current facial emotion
   - Emotion history
   - Conversation history
   ↓
5. Generate therapeutic response
   ↓
6. Store message and response in database
   ↓
7. Return response to frontend
   ↓
8. UI displays response
```

### Dashboard Flow

```
1. User switches to dashboard tab
   ↓
2. GET /api/session/<id>/emotions
   GET /api/session/<id>/stats
   ↓
3. Database queries executed
   ↓
4. Data aggregated and formatted
   ↓
5. Response sent to frontend
   ↓
6. Recharts visualizes data
   ↓
7. Auto-refresh every 5s
```

## Security Considerations

1. **Data Privacy**:
   - Images processed in-memory, not stored
   - Session data stored locally (SQLite) or in secure database
   - No user authentication (add for production)

2. **API Security**:
   - CORS configured for development
   - Input validation on all endpoints
   - Error handling to prevent information leakage

3. **Mental Health Safety**:
   - Disclaimer displayed prominently
   - Crisis detection (can be enhanced)
   - Professional help recommendations

## Scalability Considerations

1. **Horizontal Scaling**:
   - Stateless backend design
   - Database can be externalized
   - Session data can be stored in Redis

2. **Performance Optimization**:
   - Emotion detection can be async
   - Image processing can be queued
   - Database indexing on session_id and timestamp

3. **Caching**:
   - Session statistics can be cached
   - Recent conversation history cached
   - Emotion aggregation cached

## Integration Points

### OpenAI API Integration
- **Endpoint**: `https://api.openai.com/v1/chat/completions`
- **Model**: GPT-3.5-turbo or GPT-4
- **Fallback**: Rule-based responses if API unavailable
- **Cost**: Pay-per-use, can be expensive at scale

### FER Library Integration
- **Model**: Pre-trained emotion recognition model
- **Fallback**: Basic emotion estimation if FER unavailable
- **Performance**: Real-time processing capable

## Future Enhancements

1. **Authentication & User Management**
2. **Multi-user support with profiles**
3. **Advanced crisis detection**
4. **Integration with licensed therapists**
5. **Mobile app support**
6. **Voice emotion detection**
7. **Multi-language support**
8. **HIPAA compliance measures**
9. **Advanced analytics and insights**
10. **Therapist dashboard for monitoring**

## Deployment Architecture

### Development
```
Frontend (React Dev Server) :3000
    ↕ HTTP
Backend (Flask Dev Server) :5000
    ↕
SQLite Database (local file)
```

### Production
```
Nginx (Reverse Proxy)
    ↕
Flask (Gunicorn) :5000
    ↕
MongoDB / PostgreSQL
    ↕
Redis (Optional - Caching)
```

## Monitoring & Logging

- **Application Logs**: Flask logging to console/file
- **Error Tracking**: Exception handling with detailed messages
- **Performance**: Response time tracking (can be added)
- **Usage Analytics**: Session and message counts

## Compliance Considerations

- **HIPAA**: Not currently compliant (requires encryption, audit logs, etc.)
- **GDPR**: Data stored locally, user control over data
- **Mental Health Regulations**: Varies by jurisdiction
- **Disclaimer**: Required and prominently displayed

