"""
Test script for the therapeutic chatbot
Demonstrates various response scenarios
"""

from chatbot import TherapeuticChatbot

def test_chatbot():
    """Test the chatbot with various scenarios"""
    chatbot = TherapeuticChatbot()
    print("=" * 70)
    print("THERAPEUTIC CHATBOT TEST")
    print("=" * 70)
    print()
    
    test_cases = [
        {
            "name": "Greeting",
            "message": "Hello, I need someone to talk to",
            "emotion": None
        },
        {
            "name": "Stress/Anxiety",
            "message": "I've been feeling really stressed about work lately. There's just so much to do.",
            "emotion": "sad"
        },
        {
            "name": "Sadness",
            "message": "I'm just so sad all the time. Nothing seems to bring me joy anymore.",
            "emotion": "sad"
        },
        {
            "name": "Anger",
            "message": "I'm so angry at my friend. They completely let me down.",
            "emotion": "angry"
        },
        {
            "name": "Fear",
            "message": "I'm terrified about my upcoming presentation. I keep imagining everything going wrong.",
            "emotion": "fear"
        },
        {
            "name": "Emotional Mismatch",
            "message": "I'm fine, everything is okay",
            "emotion": "sad"  # User says fine but emotion shows sad
        },
        {
            "name": "General Support",
            "message": "I've been having trouble sleeping and I don't know why.",
            "emotion": "neutral"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*70}")
        print(f"User Emotion (detected): {test['emotion'] or 'None'}")
        print(f"User Message: \"{test['message']}\"")
        print(f"\n{'─'*70}")
        print("Chatbot Response:")
        print(f"{'─'*70}")
        
        response = chatbot.generate_response(
            message=test['message'],
            current_emotion=test['emotion'],
            emotion_history=None,
            conversation_history=None
        )
        
        print(response)
        print()
    
    # Test crisis detection separately
    print(f"\n{'='*70}")
    print("CRISIS DETECTION TEST")
    print(f"{'='*70}")
    crisis_messages = [
        "I don't want to live anymore",
        "I'm thinking about ending it all",
        "Life just isn't worth it"
    ]
    
    for msg in crisis_messages:
        is_crisis = chatbot.detect_crisis(msg)
        print(f"\nMessage: \"{msg}\"")
        print(f"Crisis Detected: {is_crisis}")
        if is_crisis:
            response = chatbot.generate_response(msg, current_emotion='sad')
            print(f"Response: {response[:100]}...")
    
    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print(f"{'='*70}")

if __name__ == '__main__':
    test_chatbot()

