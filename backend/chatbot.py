"""
Therapeutic Chatbot Module
Generates empathetic, therapeutic responses using GPT-based models
"""

import os
import json
from datetime import datetime
import re

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not available. Using rule-based responses.")


class TherapeuticChatbot:
    """
    Therapeutic chatbot that provides empathetic, non-judgmental responses
    Similar to responses from a licensed counselor
    """
    
    def __init__(self):
        """Initialize chatbot with therapeutic guidelines"""
        self.system_prompt = self._get_therapeutic_system_prompt()
        self.openai_client = None
        self.conversation_memory = {}  # Store conversation context per session
        
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    self.openai_client = OpenAI(api_key=api_key)
                    print("OpenAI client initialized successfully")
                except Exception as e:
                    print(f"Warning: Could not initialize OpenAI client: {e}")
            else:
                print("Warning: OPENAI_API_KEY not set. Using rule-based responses.")
    
    def _get_therapeutic_system_prompt(self):
        """Get system prompt for therapeutic responses"""
        return """You are a compassionate, empathetic AI mental health support assistant. Your role is to:

1. Provide emotional support and validation
2. Use reflective listening techniques
3. Ask open-ended questions to help users explore their feelings
4. Show empathy and understanding without judgment
5. Encourage users to express themselves safely
6. Recognize when professional help may be needed
7. Never diagnose or provide medical advice
8. Use warm, supportive, and professional language

Guidelines:
- Acknowledge the user's feelings first
- Use "I" statements when appropriate
- Avoid giving direct advice; instead, help users find their own solutions
- Be patient and allow silence/processing time
- Validate emotions without minimizing them
- Use therapeutic techniques like reflection, reframing, and normalization

Remember: You are not a replacement for professional therapy, but you can provide supportive listening and emotional validation."""

    def generate_response(self, message, current_emotion=None, emotion_history=None, conversation_history=None):
        """
        Generate therapeutic response based on message and emotional context
        
        Args:
            message: User's message
            current_emotion: Current detected emotion from facial recognition
            emotion_history: List of recent emotions
            conversation_history: Previous conversation messages
        
        Returns:
            Therapeutic response string
        """
        # Analyze sentiment and emotional state
        sentiment = self._analyze_sentiment(message)
        emotional_context = self._build_emotional_context(current_emotion, emotion_history)
        
        # Use OpenAI if available, otherwise use rule-based
        if self.openai_client:
            return self._generate_openai_response(message, sentiment, emotional_context, conversation_history)
        else:
            return self._generate_rule_based_response(message, sentiment, emotional_context)
    
    def _analyze_sentiment(self, message):
        """Analyze sentiment of the message with enhanced keyword detection"""
        message_lower = message.lower()
        
        # Enhanced keywords for different emotional states
        stress_keywords = ['stressed', 'overwhelmed', 'pressure', 'anxious', 'worried', 'panic', 
                          'tension', 'nervous', 'worries', 'stressing', 'overwhelm']
        sadness_keywords = ['sad', 'depressed', 'down', 'hopeless', 'empty', 'lonely', 'miserable',
                           'unhappy', 'sorrow', 'grief', 'melancholy', 'blue', 'downhearted']
        anger_keywords = ['angry', 'furious', 'mad', 'frustrated', 'annoyed', 'irritated', 'rage',
                         'livid', 'enraged', 'resentful', 'bitter', 'hostile']
        fear_keywords = ['afraid', 'scared', 'fear', 'terrified', 'worried', 'nervous', 'anxious',
                        'panic', 'dread', 'apprehensive', 'frightened', 'intimidated']
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'not worth living', 'want to die',
                          'hurt myself', 'self harm', 'cutting', 'overdose']
        
        sentiment = {
            'crisis': sum(1 for phrase in crisis_keywords if phrase in message_lower),
            'stress': sum(1 for word in stress_keywords if word in message_lower),
            'sadness': sum(1 for word in sadness_keywords if word in message_lower),
            'anger': sum(1 for word in anger_keywords if word in message_lower),
            'fear': sum(1 for word in fear_keywords if word in message_lower),
            'neutral': 0
        }
        
        # Check for crisis first (highest priority)
        if sentiment['crisis'] > 0:
            return 'crisis'
        
        max_sentiment = max([(k, v) for k, v in sentiment.items() if k != 'crisis'], key=lambda x: x[1])
        return max_sentiment[0] if max_sentiment[1] > 0 else 'neutral'
    
    def _build_emotional_context(self, current_emotion, emotion_history):
        """Build emotional context from facial recognition data"""
        context = {
            'current': current_emotion if current_emotion else None,
            'recent_pattern': None
        }
        
        if emotion_history and len(emotion_history) > 0:
            recent_emotions = [e.get('dominant_emotion', 'neutral') for e in emotion_history[-5:]]
            if recent_emotions:
                from collections import Counter
                most_common = Counter(recent_emotions).most_common(1)
                context['recent_pattern'] = most_common[0][0] if most_common else None
        
        return context
    
    def _generate_openai_response(self, message, sentiment, emotional_context, conversation_history):
        """Generate response using OpenAI API (v1.0+)"""
        try:
            # Build conversation context
            system_content = self.system_prompt
            
            # Add emotional context to system message
            if emotional_context['current'] or emotional_context['recent_pattern']:
                context_note = "\n\nUser's current emotional state: "
                if emotional_context['current']:
                    context_note += f"detected emotion: {emotional_context['current']}. "
                if emotional_context['recent_pattern']:
                    context_note += f"Recent emotional pattern: {emotional_context['recent_pattern']}. "
                system_content += context_note
            
            # Add crisis detection warning if needed
            if sentiment == 'crisis':
                system_content += "\n\n⚠️ CRISIS DETECTED: The user may be in crisis. Respond with immediate concern, validation, and provide crisis resources. Be supportive but also encourage professional help."
            
            messages = [{"role": "system", "content": system_content}]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    role = "user" if msg.get('role') == 'user' else "assistant"
                    messages.append({"role": role, "content": msg.get('content', '')})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API (new format)
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based
            return self._generate_rule_based_response(message, sentiment, emotional_context)
    
    def _generate_rule_based_response(self, message, sentiment, emotional_context):
        """Generate therapeutic response using rule-based logic"""
        message_lower = message.lower()
        
        # CRISIS DETECTION - Highest priority
        if sentiment == 'crisis':
            crisis_responses = [
                "I'm really concerned about what you're sharing. Your life has value, and there are people who want to help. Please reach out to a crisis helpline right now: National Suicide Prevention Lifeline at 988, or Crisis Text Line by texting HOME to 741741. You don't have to go through this alone.",
                "I hear that you're in a lot of pain right now, and I'm worried about you. Please know that there is help available. If you're in immediate danger, please call 911 or go to your nearest emergency room. You can also call the National Suicide Prevention Lifeline at 988 - they're available 24/7.",
                "Thank you for sharing this with me. I want you to know that your feelings are valid, but I'm very concerned about your safety. Please reach out for immediate professional help. Call 988 (Suicide Prevention Lifeline) or 911 if you're in immediate danger. There are people trained to help you through this."
            ]
            return self._select_response(crisis_responses, emotional_context)
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start', 'begin']):
            greeting_responses = [
                "Hello. I'm here to listen and support you. How are you feeling today? You can share whatever's on your mind, and I'll be here with you.",
                "Hi there. Thank you for reaching out. I'm here to provide a safe space for you to express yourself. What's on your mind today?",
                "Hello. I'm glad you're here. This is a judgment-free space where you can share your thoughts and feelings. How are you doing today?"
            ]
            return self._select_response(greeting_responses, emotional_context)
        
        # Stress/Anxiety responses
        if sentiment == 'stress' or 'stressed' in message_lower or 'anxious' in message_lower:
            responses = [
                "I can hear that you're feeling stressed right now. That sounds really difficult. Can you tell me more about what's contributing to these feelings?",
                "It sounds like you're experiencing a lot of pressure. That must be overwhelming. What would help you feel a bit more grounded right now?",
                "I understand that stress can feel consuming. You're not alone in feeling this way. What's one thing that's been weighing on you the most?"
            ]
            return self._select_response(responses, emotional_context)
        
        # Sadness responses
        if sentiment == 'sadness' or 'sad' in message_lower or 'depressed' in message_lower:
            responses = [
                "I hear the sadness in what you're sharing. Thank you for trusting me with these feelings. Can you help me understand what's been making you feel this way?",
                "It sounds like you're going through a really tough time. Your feelings are valid, and I'm here to listen. What's been on your mind lately?",
                "I can sense that you're feeling down. That must be really hard. Would you like to talk about what's been contributing to these feelings?"
            ]
            return self._select_response(responses, emotional_context)
        
        # Anger responses
        if sentiment == 'anger' or 'angry' in message_lower or 'frustrated' in message_lower:
            responses = [
                "I can hear the frustration in your words. It sounds like something has really upset you. Can you help me understand what happened?",
                "It seems like you're feeling angry, and that's completely understandable. What's been making you feel this way?",
                "I hear that you're frustrated. Those feelings are valid. Would you like to talk about what's been bothering you?"
            ]
            return self._select_response(responses, emotional_context)
        
        # Fear responses
        if sentiment == 'fear' or 'afraid' in message_lower or 'scared' in message_lower:
            responses = [
                "I can sense that you're feeling afraid or worried. That must be really unsettling. Can you tell me more about what's causing these feelings?",
                "It sounds like fear is really present for you right now. That's a difficult emotion to sit with. What would help you feel a bit safer?",
                "I hear that you're feeling scared. Thank you for sharing that with me. What's been making you feel this way?"
            ]
            return self._select_response(responses, emotional_context)
        
        # Questions about feelings
        if any(word in message_lower for word in ['feel', 'feeling', 'emotion']):
            return "I appreciate you sharing how you're feeling. Can you tell me more about what's behind these feelings? Sometimes exploring them can help us understand ourselves better."
        
        # General empathetic responses
        if len(message.split()) < 5:
            return "I'm listening. Can you tell me more about what's on your mind?"
        
        # Check for emotional mismatch (user says fine but emotion shows otherwise)
        if emotional_context['current'] and emotional_context['current'] != 'neutral':
            if 'fine' in message_lower or 'okay' in message_lower or 'ok' in message_lower:
                mismatch_responses = [
                    f"I hear you say you're doing okay, and I want to respect that. I'm also noticing that you might be feeling {emotional_context['current']} right now. Sometimes it can be hard to put words to our feelings. Would you like to talk about what's going on?",
                    "Thank you for sharing. I want to acknowledge that sometimes our words and our feelings don't always match up, and that's okay. If you'd like to explore what you're experiencing, I'm here to listen.",
                    "I hear you, and I also notice there might be more going on beneath the surface. Would you like to talk about what you're really feeling right now?"
                ]
                return self._select_response(mismatch_responses, emotional_context)
        
        # Reflective responses with better context awareness
        responses = [
            "Thank you for sharing that with me. It sounds like that's been really significant for you. Can you help me understand more about how that's been affecting you?",
            "I hear what you're saying. It sounds like this is something that's been on your mind. Can you tell me more about what that's been like for you?",
            "That sounds really important to you. What's it been like for you to experience that?",
            "I appreciate you opening up about this. How have you been coping with these feelings?",
            "It sounds like this has been weighing on you. What would it mean for you if things were different?",
            "I'm listening, and I want to make sure I understand. Can you help me see this from your perspective?",
            "That sounds challenging. What's been the hardest part about this for you?",
            "Thank you for trusting me with this. What do you think might help you feel a bit better?"
        ]
        
        return self._select_response(responses, emotional_context)
    
    def _select_response(self, responses, emotional_context):
        """Select appropriate response based on context"""
        import random
        
        # If we have emotional context, try to match response tone
        if emotional_context['current']:
            emotion = emotional_context['current']
            # Filter responses that might be more appropriate for the emotion
            # For now, we'll use random but could enhance with semantic matching
            pass
        
        return random.choice(responses)
    
    def detect_crisis(self, message):
        """Detect if message indicates a mental health crisis"""
        message_lower = message.lower()
        crisis_indicators = [
            'suicide', 'kill myself', 'end it all', 'not worth living',
            'want to die', 'hurt myself', 'self harm', 'cutting',
            'overdose', 'no point', 'give up', 'end my life'
        ]
        return any(indicator in message_lower for indicator in crisis_indicators)


if __name__ == '__main__':
    chatbot = TherapeuticChatbot()
    print("Therapeutic chatbot initialized successfully")
    
    # Test response
    test_message = "I've been feeling really stressed about work lately"
    response = chatbot.generate_response(test_message, current_emotion='sad')
    print(f"\nTest Message: {test_message}")
    print(f"Response: {response}")

