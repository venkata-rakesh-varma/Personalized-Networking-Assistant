import requests
from typing import List, Optional
from app.config import MODEL_NAMES, HF_API_KEY

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAMES['event_analysis']}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def extract_event_themes(description: str, candidate_labels: Optional[List[str]] = None) -> List[str]:
    if candidate_labels is None:
        candidate_labels = ["AI", "healthcare", "blockchain", "education", "sustainability"]
    
    payload = {
        "inputs": description,
        "parameters": {"candidate_labels": candidate_labels}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("labels", [])[:3]  # Return top 3 themes
    else:
        print(f"API Error: {response.text}")
        return ["Networking", "Professional Development", "Technology"] # Fallback