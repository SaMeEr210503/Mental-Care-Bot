"""
Flask Backend for AI-based Mental Health Monitoring and Support System
Main application file with API endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
from datetime import datetime
import base64
import cv2
import numpy as np

from emotion_detector import EmotionDetector
from chatbot import TherapeuticChatbot
from database import Database

# Serve React build in production
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'build')
if os.path.exists(static_folder):
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
else:
    app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
emotion_detector = EmotionDetector()
chatbot = TherapeuticChatbot()
db = Database()

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def serve():
    """Serve React frontend"""
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({'message': 'Frontend not built. Please run npm build in frontend directory.'})


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/emotion/detect', methods=['POST'])
def detect_emotion():
    """
    Detect emotions from image data
    Expects base64 encoded image in request
    """
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Detect emotions
        result = emotion_detector.detect_emotions(image)
        
        # Store emotion log if session_id provided
        session_id = data.get('session_id')
        if session_id:
            db.log_emotion(session_id, result)
        
        return jsonify({
            'success': True,
            'emotions': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """
    Handle chat messages and generate therapeutic responses
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        current_emotion = data.get('current_emotion')  # From facial detection
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Create session if doesn't exist
        if not session_id:
            session_id = db.create_session()
        
        # Store user message
        db.add_message(session_id, 'user', message)
        
        # Get recent emotion history for context
        emotion_history = db.get_recent_emotions(session_id, limit=5) if session_id else []
        
        # Check for crisis indicators
        is_crisis = chatbot.detect_crisis(message)
        
        # Generate therapeutic response
        response = chatbot.generate_response(
            message=message,
            current_emotion=current_emotion,
            emotion_history=emotion_history,
            conversation_history=db.get_conversation_history(session_id)
        )
        
        # Store bot response
        db.add_message(session_id, 'assistant', response)
        
        return jsonify({
            'success': True,
            'response': response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'crisis_detected': is_crisis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Create a new therapy session"""
    try:
        session_id = db.create_session()
        return jsonify({
            'success': True,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/<session_id>/history', methods=['GET'])
def get_session_history(session_id):
    """Get conversation history for a session"""
    try:
        messages = db.get_conversation_history(session_id)
        return jsonify({
            'success': True,
            'messages': messages,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/<session_id>/emotions', methods=['GET'])
def get_emotion_history(session_id):
    """Get emotion history for a session"""
    try:
        limit = request.args.get('limit', 100, type=int)
        emotions = db.get_emotion_history(session_id, limit=limit)
        return jsonify({
            'success': True,
            'emotions': emotions,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/<session_id>/stats', methods=['GET'])
def get_session_stats(session_id):
    """Get aggregated statistics for a session"""
    try:
        stats = db.get_session_stats(session_id)
        return jsonify({
            'success': True,
            'stats': stats,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors for React routing"""
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    print("Starting Mental Health Support System...")
    print("Backend server running on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

