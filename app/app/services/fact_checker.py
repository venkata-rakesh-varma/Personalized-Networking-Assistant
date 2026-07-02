# app/services/fact_checker.py

import requests
from app.config import FACT_CHECK_API


def fact_check(query: str) -> str:
    try:
        response = requests.get(f"{FACT_CHECK_API}/{query}")
        data = response.json()
        return data.get("extract", "No summary found.")
    except:
        return "Fact-checking failed."