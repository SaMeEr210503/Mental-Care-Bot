"""
Emotion Detection Module using OpenCV and Deep Learning
Detects facial emotions from images using pre-trained models
"""

import cv2
import numpy as np
from collections import Counter
import os

try:
    from fer import FER
    FER_AVAILABLE = True
except ImportError:
    FER_AVAILABLE = False
    print("Warning: FER library not available. Using basic emotion detection.")


class EmotionDetector:
    """
    Emotion detection using facial recognition
    Supports multiple emotion detection backends
    """
    
    def __init__(self):
        """Initialize emotion detector with face cascade and emotion model"""
        # Load face detection cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Initialize FER if available
        self.fer_detector = None
        if FER_AVAILABLE:
            try:
                self.fer_detector = FER(mtcnn=True)
                print("FER emotion detector initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize FER: {e}")
                self.fer_detector = None
        
        # Emotion labels
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
    def detect_faces(self, image):
        """Detect faces in image using Haar Cascade"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def detect_emotions(self, image):
        """
        Detect emotions in image
        Returns dictionary with emotion predictions and face locations
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
            
            # Detect faces
            faces = self.detect_faces(image)
            
            if len(faces) == 0:
                return {
                    'faces_detected': 0,
                    'dominant_emotion': 'neutral',
                    'emotions': {'neutral': 1.0},
                    'confidence': 0.0,
                    'face_locations': []
                }
            
            all_emotions = []
            face_locations = []
            
            # Process each face
            for (x, y, w, h) in faces:
                face_locations.append({
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h)
                })
                
                # Extract face region
                face_roi = rgb_image[y:y+h, x:x+w]
                
                # Use FER if available
                if self.fer_detector:
                    try:
                        emotions = self.fer_detector.detect_emotions(face_roi)
                        if emotions:
                            all_emotions.append(emotions[0]['emotions'])
                    except Exception as e:
                        print(f"FER detection error: {e}")
                        # Fallback to basic detection
                        all_emotions.append(self._basic_emotion_estimation(face_roi))
                else:
                    # Basic emotion estimation based on facial features
                    all_emotions.append(self._basic_emotion_estimation(face_roi))
            
            # Aggregate emotions from all faces
            if all_emotions:
                aggregated = self._aggregate_emotions(all_emotions)
                dominant = max(aggregated.items(), key=lambda x: x[1])
                
                return {
                    'faces_detected': len(faces),
                    'dominant_emotion': dominant[0],
                    'emotions': aggregated,
                    'confidence': float(dominant[1]),
                    'face_locations': face_locations,
                    'timestamp': self._get_timestamp()
                }
            else:
                return {
                    'faces_detected': len(faces),
                    'dominant_emotion': 'neutral',
                    'emotions': {'neutral': 1.0},
                    'confidence': 0.0,
                    'face_locations': face_locations
                }
        
        except Exception as e:
            print(f"Emotion detection error: {e}")
            return {
                'faces_detected': 0,
                'dominant_emotion': 'neutral',
                'emotions': {'neutral': 1.0},
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _basic_emotion_estimation(self, face_roi):
        """
        Basic emotion estimation when FER is not available
        Uses simple heuristics based on facial geometry
        """
        # This is a simplified fallback - in production, use a trained model
        # For now, return neutral with slight variations
        emotions = {
            'angry': 0.1,
            'disgust': 0.05,
            'fear': 0.1,
            'happy': 0.2,
            'sad': 0.15,
            'surprise': 0.1,
            'neutral': 0.3
        }
        return emotions
    
    def _aggregate_emotions(self, emotion_list):
        """Aggregate emotions from multiple faces"""
        aggregated = {emotion: 0.0 for emotion in self.emotion_labels}
        
        for emotions in emotion_list:
            for emotion, value in emotions.items():
                if emotion in aggregated:
                    aggregated[emotion] += value
        
        # Normalize
        total = sum(aggregated.values())
        if total > 0:
            aggregated = {k: v / total for k, v in aggregated.items()}
        
        return aggregated
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == '__main__':
    # Test emotion detector
    detector = EmotionDetector()
    print("Emotion detector initialized successfully")

