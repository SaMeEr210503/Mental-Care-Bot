# AI-Based Mental Health Monitoring and Support System

A full-stack application that combines facial emotion recognition with an AI-powered therapeutic chatbot to provide real-time mental health monitoring and emotional support.

## Features

- **Real-time Emotion Detection**: Uses OpenCV and deep learning models to detect facial emotions from webcam feed
- **Therapeutic Chatbot**: GPT-based conversational AI that responds with empathy, using therapeutic techniques like reflective listening
- **Emotion Analytics Dashboard**: Visualizes emotional patterns over time with interactive charts
- **Session Management**: Tracks conversations and emotions across therapy sessions
- **Professional Design**: Calming, minimalist UI designed for mental health support

## Architecture

### Backend (Flask)
- **app.py**: Main Flask application with REST API endpoints
- **emotion_detector.py**: Face detection and emotion recognition using OpenCV and FER
- **chatbot.py**: Therapeutic response generation with GPT integration
- **database.py**: Database abstraction layer supporting MongoDB and SQLite

### Frontend (React)
- **WebcamCapture**: Live video feed with real-time emotion detection
- **ChatInterface**: Conversational interface for AI therapy sessions
- **EmotionDashboard**: Analytics and visualization of emotional patterns
- **Disclaimer**: Mental health disclaimer and safety notices

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Webcam access
- (Optional) OpenAI API key for GPT-based responses
- (Optional) MongoDB for production database

## Installation

### Backend Setup

1. Navigate to the project root directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

4. Set up environment variables (optional):
```bash
# Create .env file in backend directory
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb://localhost:27017/  # Optional, defaults to SQLite
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
python app.py
```

The backend will run on `http://localhost:5000`

### Start Frontend Development Server

In a new terminal:
```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## Usage

1. **Start a Session**: The application automatically creates a new therapy session when you open it.

2. **Enable Camera**: Click "Start Camera" to begin real-time emotion detection. The system will analyze your facial expressions every 2 seconds.

3. **Chat with AI**: Type your thoughts and feelings in the chat interface. The AI will respond with empathetic, therapeutic responses.

4. **View Analytics**: Switch to the "Emotion Dashboard" tab to see:
   - Emotion trends over time
   - Distribution of detected emotions
   - Session statistics

## Database Schema

### Sessions Table
- `session_id` (Primary Key): Unique session identifier
- `created_at`: Session creation timestamp
- `updated_at`: Last update timestamp

### Messages Table
- `id` (Primary Key): Auto-incrementing ID
- `session_id` (Foreign Key): Links to session
- `role`: 'user' or 'assistant'
- `content`: Message text
- `timestamp`: Message timestamp

### Emotions Table
- `id` (Primary Key): Auto-incrementing ID
- `session_id` (Foreign Key): Links to session
- `dominant_emotion`: Primary detected emotion
- `emotions`: JSON object with all emotion scores
- `confidence`: Detection confidence score
- `faces_detected`: Number of faces detected
- `timestamp`: Detection timestamp

## API Endpoints

### Health Check
- `GET /api/health` - Check server status

### Sessions
- `POST /api/session/create` - Create new session
- `GET /api/session/<session_id>/history` - Get conversation history
- `GET /api/session/<session_id>/emotions` - Get emotion history
- `GET /api/session/<session_id>/stats` - Get session statistics

### Emotion Detection
- `POST /api/emotion/detect` - Detect emotions from image

### Chat
- `POST /api/chat/message` - Send message and get AI response

## Therapeutic Response Design

The chatbot is designed to:

- **Show Empathy**: Acknowledge and validate user feelings
- **Use Reflective Listening**: Paraphrase and reflect back what users share
- **Ask Open-Ended Questions**: Encourage exploration of feelings
- **Avoid Judgment**: Create a safe, non-judgmental space
- **Recognize Limits**: Know when to suggest professional help
- **Integrate Context**: Use both facial emotions and chat sentiment to tailor responses

### Example Responses

**User**: "I've been feeling really stressed about work lately"

**AI**: "I can hear that you're feeling stressed right now. That sounds really difficult. Can you tell me more about what's contributing to these feelings?"

**User**: "I'm just so sad all the time"

**AI**: "I hear the sadness in what you're sharing. Thank you for trusting me with these feelings. Can you help me understand what's been making you feel this way?"

## Important Disclaimers

⚠️ **This AI-powered system is designed to provide emotional support and monitoring. It is NOT a substitute for professional therapy, medical advice, or mental health treatment.**

If you are experiencing a mental health emergency, please contact:
- Your local emergency services (911 in US)
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741 (US)
- Your local mental health professional

## Technology Stack

### Backend
- Flask: Web framework
- OpenCV: Computer vision and face detection
- FER: Facial Expression Recognition library
- OpenAI API: GPT-based conversational AI (optional)
- SQLite/MongoDB: Database storage

### Frontend
- React: UI framework
- Axios: HTTP client
- Recharts: Data visualization
- WebRTC: Webcam access

## Development

### Project Structure
```
.
├── backend/
│   ├── app.py              # Flask application
│   ├── emotion_detector.py # Emotion detection module
│   ├── chatbot.py          # Therapeutic chatbot
│   └── database.py         # Database handler
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main app component
│   │   └── index.js        # Entry point
│   └── package.json
├── requirements.txt        # Python dependencies
└── README.md
```

## Troubleshooting

### Camera Not Working
- Ensure browser permissions are granted for camera access
- Check that no other application is using the camera
- Try a different browser (Chrome recommended)

### Emotion Detection Not Accurate
- Ensure good lighting
- Face the camera directly
- Remove obstructions (glasses, masks, etc.)

### OpenAI API Errors
- Verify your API key is set correctly
- Check your API quota/credits
- The system will fall back to rule-based responses if API is unavailable

## License

This project is for educational and research purposes. Please ensure compliance with all applicable laws and regulations regarding mental health services in your jurisdiction.

## Contributing

This is a demonstration project. For production use, consider:
- Adding user authentication
- Implementing data encryption
- Adding HIPAA compliance measures
- Integrating with licensed mental health professionals
- Adding more sophisticated emotion detection models
- Implementing crisis detection and intervention protocols

## Acknowledgments

- FER library for emotion recognition
- OpenAI for GPT models
- OpenCV community for computer vision tools

