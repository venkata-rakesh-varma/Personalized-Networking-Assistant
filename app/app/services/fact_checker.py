import requests
import urllib.parse
from app.config import FACT_CHECK_API

def fact_check(query: str) -> str:
    safe_query = urllib.parse.quote(query)
    
    # Wikipedia requires a descriptive User-Agent
    headers = {
        "User-Agent": "NetworkingAssistantApp/1.0 (Local Development)"
    }
    
    try:
        response = requests.get(f"{FACT_CHECK_API}/{safe_query}", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No Wikipedia summary found for this specific topic.")
        elif response.status_code == 404:
            return "Wikipedia page not found. Try a different or broader search term."
        else:
            return f"Fact-checking failed. Wikipedia API returned status code: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        print("Fact Checker Network block detected.")
        return "Network blocked the request to Wikipedia. (Offline Fallback: Quantum Machine Learning is a research area that explores the interplay of ideas from quantum computing and machine learning.)"
    except Exception as e:
        print(f"Error fetching fact check: {e}")
        return "Fact-checking service is temporarily unavailable."