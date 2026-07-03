import requests
from app.config import MODEL_NAMES, HF_API_KEY

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAMES['text_generator']}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_topics(event_themes, user_interests):
    prompt = (
        f"I'm attending a networking event focused on {', '.join(event_themes)}. "
        f"I'm personally interested in {', '.join(user_interests)}. "
        f"What are three creative and engaging conversation starters I could use to break the ice?"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 80,
            "return_full_text": False 
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            generated_text = data[0].get("generated_text", "")
            suggestions = generated_text.split("\n")[:3]
            return [s.strip("- ").strip() for s in suggestions if s.strip()]
    
    print(f"API Error: {response.text}")
    return ["What brings you to this event today?", "Have you heard any good talks so far?"] # Fallback