# Chatbot Enhancements

## Overview

The therapeutic chatbot has been significantly enhanced with improved functionality, better crisis detection, and more sophisticated response generation.

## Key Improvements

### 1. **Updated OpenAI Integration**
- Migrated to OpenAI API v1.0+ format
- Proper error handling and fallback mechanisms
- Better initialization with try-catch blocks

### 2. **Enhanced Sentiment Analysis**
- Expanded keyword detection for emotions:
  - **Stress**: Added 'tension', 'nervous', 'worries', 'stressing', 'overwhelm'
  - **Sadness**: Added 'miserable', 'unhappy', 'sorrow', 'grief', 'melancholy', 'blue', 'downhearted'
  - **Anger**: Added 'rage', 'livid', 'enraged', 'resentful', 'bitter', 'hostile'
  - **Fear**: Added 'dread', 'apprehensive', 'frightened', 'intimidated'
- More accurate emotion detection

### 3. **Crisis Detection System**
- **Priority Detection**: Crisis keywords are checked first (highest priority)
- **Crisis Keywords**: Detects phrases like:
  - 'suicide', 'kill myself', 'end it all'
  - 'not worth living', 'want to die'
  - 'hurt myself', 'self harm', 'cutting', 'overdose'
- **Immediate Response**: Provides crisis resources when detected:
  - National Suicide Prevention Lifeline: 988
  - Crisis Text Line: Text HOME to 741741
  - Emergency services: 911
- **Frontend Integration**: Crisis messages are highlighted and alerts are shown

### 4. **Emotional Context Integration**
- **Mismatch Detection**: Identifies when user says "I'm fine" but facial emotion shows otherwise
- **Context-Aware Responses**: Uses both facial emotion and text sentiment
- **Pattern Recognition**: Analyzes recent emotional patterns from emotion history

### 5. **Improved Response Quality**
- **More Varied Responses**: Expanded response pool for each emotion category
- **Better Greetings**: Multiple greeting variations
- **Enhanced Reflective Responses**: More sophisticated therapeutic responses
- **Context Matching**: Responses adapt based on emotional context

### 6. **API Enhancements**
- **Crisis Flag**: API now returns `crisis_detected` boolean
- **Better Error Handling**: Graceful fallbacks when OpenAI API is unavailable
- **Session Memory**: Conversation context stored per session

## Response Examples

### Crisis Response
**User**: "I don't want to live anymore"

**Chatbot**: "I'm really concerned about what you're sharing. Your life has value, and there are people who want to help. Please reach out to a crisis helpline right now: National Suicide Prevention Lifeline at 988, or Crisis Text Line by texting HOME to 741741. You don't have to go through this alone."

### Emotional Mismatch Detection
**User**: "I'm fine, everything is okay" (while facial emotion shows sadness)

**Chatbot**: "I hear you say you're doing okay, and I want to respect that. I'm also noticing that you might be feeling sad right now. Sometimes it can be hard to put words to our feelings. Would you like to talk about what's going on?"

### Enhanced Stress Response
**User**: "I've been feeling really stressed about work lately"

**Chatbot**: "I can hear that you're feeling stressed right now. That sounds really difficult. Can you tell me more about what's contributing to these feelings?"

## Testing

Run the test script to see the chatbot in action:

```bash
cd backend
python test_chatbot.py
```

This will demonstrate:
- Various emotional scenarios
- Crisis detection
- Emotional mismatch handling
- Response quality

## Technical Details

### File Structure
- `backend/chatbot.py`: Main chatbot implementation
- `backend/test_chatbot.py`: Test script
- `backend/app.py`: API endpoint with crisis detection
- `frontend/src/components/ChatInterface.js`: Frontend with crisis alerts

### Dependencies
- OpenAI library (v1.0+): `from openai import OpenAI`
- Fallback: Rule-based responses when OpenAI unavailable

### Configuration
Set environment variable for OpenAI:
```bash
export OPENAI_API_KEY=your_key_here
```

Or create `.env` file in backend directory:
```
OPENAI_API_KEY=your_key_here
```

## Safety Features

1. **Crisis Detection**: Automatically detects crisis situations
2. **Resource Provision**: Provides immediate crisis resources
3. **Professional Help Encouragement**: Always encourages professional help when needed
4. **Non-Judgmental**: Maintains empathetic, supportive tone
5. **Disclaimer**: Clear disclaimers about limitations

## Future Enhancements

Potential improvements:
- Machine learning-based sentiment analysis
- Multi-language support
- Voice emotion detection integration
- Advanced pattern recognition
- Therapist referral system
- Session summary generation
- Progress tracking

## Usage

The chatbot is automatically initialized when the Flask backend starts. It works in two modes:

1. **OpenAI Mode** (if API key provided): Uses GPT-3.5-turbo for responses
2. **Rule-Based Mode** (fallback): Uses sophisticated rule-based responses

Both modes provide therapeutic, empathetic responses with crisis detection.

