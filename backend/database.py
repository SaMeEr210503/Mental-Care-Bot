"""
Database Module for storing sessions, messages, and emotion logs
Supports both MongoDB and SQLite
"""

import os
import json
from datetime import datetime
import uuid

try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False


class Database:
    """
    Database handler for mental health support system
    Supports MongoDB (preferred) and SQLite (fallback)
    """
    
    def __init__(self, db_type='sqlite', connection_string=None):
        """
        Initialize database connection
        
        Args:
            db_type: 'mongodb' or 'sqlite'
            connection_string: MongoDB connection string or SQLite file path
        """
        self.db_type = db_type.lower()
        self.connection_string = connection_string
        
        if self.db_type == 'mongodb' and MONGODB_AVAILABLE:
            self._init_mongodb()
        elif self.db_type == 'sqlite' and SQLITE_AVAILABLE:
            self._init_sqlite()
        else:
            # Default to SQLite
            self.db_type = 'sqlite'
            self._init_sqlite()
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            if not self.connection_string:
                self.connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            
            self.client = MongoClient(self.connection_string)
            self.db = self.client['mental_health_support']
            self.sessions = self.db['sessions']
            self.messages = self.db['messages']
            self.emotions = self.db['emotions']
            
            # Create indexes
            self.messages.create_index('session_id')
            self.emotions.create_index('session_id')
            self.emotions.create_index('timestamp')
            
            print("MongoDB initialized successfully")
        except Exception as e:
            print(f"MongoDB initialization error: {e}, falling back to SQLite")
            self.db_type = 'sqlite'
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        db_path = self.connection_string or 'mental_health.db'
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create tables
        self._create_tables()
        print(f"SQLite database initialized: {db_path}")
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        # Sessions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Messages table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        # Emotions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                dominant_emotion TEXT,
                emotions TEXT,
                confidence REAL,
                faces_detected INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        # Create indexes
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotions_session ON emotions(session_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotions_timestamp ON emotions(timestamp)')
        
        self.conn.commit()
    
    def create_session(self):
        """Create a new therapy session"""
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if self.db_type == 'mongodb':
            self.sessions.insert_one({
                'session_id': session_id,
                'created_at': timestamp,
                'updated_at': timestamp
            })
        else:
            self.cursor.execute(
                'INSERT INTO sessions (session_id, created_at, updated_at) VALUES (?, ?, ?)',
                (session_id, timestamp, timestamp)
            )
            self.conn.commit()
        
        return session_id
    
    def add_message(self, session_id, role, content):
        """Add a message to the conversation"""
        timestamp = datetime.now().isoformat()
        
        if self.db_type == 'mongodb':
            self.messages.insert_one({
                'session_id': session_id,
                'role': role,
                'content': content,
                'timestamp': timestamp
            })
            # Update session
            self.sessions.update_one(
                {'session_id': session_id},
                {'$set': {'updated_at': timestamp}}
            )
        else:
            self.cursor.execute(
                'INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)',
                (session_id, role, content, timestamp)
            )
            self.cursor.execute(
                'UPDATE sessions SET updated_at = ? WHERE session_id = ?',
                (timestamp, session_id)
            )
            self.conn.commit()
    
    def get_conversation_history(self, session_id, limit=100):
        """Get conversation history for a session"""
        if self.db_type == 'mongodb':
            messages = list(self.messages.find(
                {'session_id': session_id}
            ).sort('timestamp', 1).limit(limit))
            return [{'role': m['role'], 'content': m['content'], 'timestamp': m['timestamp']} for m in messages]
        else:
            self.cursor.execute(
                'SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?',
                (session_id, limit)
            )
            rows = self.cursor.fetchall()
            return [{'role': row[0], 'content': row[1], 'timestamp': row[2]} for row in rows]
    
    def log_emotion(self, session_id, emotion_data):
        """Log detected emotion"""
        timestamp = datetime.now().isoformat()
        dominant_emotion = emotion_data.get('dominant_emotion', 'neutral')
        emotions_json = json.dumps(emotion_data.get('emotions', {}))
        confidence = emotion_data.get('confidence', 0.0)
        faces_detected = emotion_data.get('faces_detected', 0)
        
        if self.db_type == 'mongodb':
            self.emotions.insert_one({
                'session_id': session_id,
                'dominant_emotion': dominant_emotion,
                'emotions': emotion_data.get('emotions', {}),
                'confidence': confidence,
                'faces_detected': faces_detected,
                'timestamp': timestamp
            })
        else:
            self.cursor.execute(
                '''INSERT INTO emotions (session_id, dominant_emotion, emotions, confidence, faces_detected, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (session_id, dominant_emotion, emotions_json, confidence, faces_detected, timestamp)
            )
            self.conn.commit()
    
    def get_recent_emotions(self, session_id, limit=10):
        """Get recent emotion detections for a session"""
        if self.db_type == 'mongodb':
            emotions = list(self.emotions.find(
                {'session_id': session_id}
            ).sort('timestamp', -1).limit(limit))
            return [{
                'dominant_emotion': e['dominant_emotion'],
                'emotions': e.get('emotions', {}),
                'confidence': e.get('confidence', 0.0),
                'timestamp': e['timestamp']
            } for e in emotions]
        else:
            self.cursor.execute(
                'SELECT dominant_emotion, emotions, confidence, timestamp FROM emotions WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
                (session_id, limit)
            )
            rows = self.cursor.fetchall()
            return [{
                'dominant_emotion': row[0],
                'emotions': json.loads(row[1]) if row[1] else {},
                'confidence': row[2],
                'timestamp': row[3]
            } for row in rows]
    
    def get_emotion_history(self, session_id, limit=100):
        """Get emotion history for a session"""
        return self.get_recent_emotions(session_id, limit)
    
    def get_session_stats(self, session_id):
        """Get aggregated statistics for a session"""
        if self.db_type == 'mongodb':
            # Get emotion counts
            pipeline = [
                {'$match': {'session_id': session_id}},
                {'$group': {
                    '_id': '$dominant_emotion',
                    'count': {'$sum': 1},
                    'avg_confidence': {'$avg': '$confidence'}
                }}
            ]
            emotion_stats = list(self.emotions.aggregate(pipeline))
            
            # Get message count
            message_count = self.messages.count_documents({'session_id': session_id})
            
            # Get session info
            session = self.sessions.find_one({'session_id': session_id})
            
        else:
            # Get emotion counts
            self.cursor.execute('''
                SELECT dominant_emotion, COUNT(*) as count, AVG(confidence) as avg_confidence
                FROM emotions
                WHERE session_id = ?
                GROUP BY dominant_emotion
            ''', (session_id,))
            emotion_stats = [
                {'_id': row[0], 'count': row[1], 'avg_confidence': row[2]}
                for row in self.cursor.fetchall()
            ]
            
            # Get message count
            self.cursor.execute(
                'SELECT COUNT(*) FROM messages WHERE session_id = ?',
                (session_id,)
            )
            message_count = self.cursor.fetchone()[0]
            
            # Get session info
            self.cursor.execute(
                'SELECT created_at, updated_at FROM sessions WHERE session_id = ?',
                (session_id,)
            )
            session_row = self.cursor.fetchone()
            session = {
                'created_at': session_row[0] if session_row else None,
                'updated_at': session_row[1] if session_row else None
            } if session_row else None
        
        return {
            'session_id': session_id,
            'emotion_distribution': {stat['_id']: {'count': stat['count'], 'avg_confidence': stat['avg_confidence']} for stat in emotion_stats},
            'message_count': message_count,
            'created_at': session['created_at'] if session else None,
            'updated_at': session['updated_at'] if session else None
        }


if __name__ == '__main__':
    db = Database()
    print("Database initialized successfully")
    
    # Test
    session_id = db.create_session()
    print(f"Created test session: {session_id}")

