import google.auth
from google.auth.transport.requests import Request
import requests
import os

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")

def get_daily_tech_news():
    payload = {
        "contents": [{
            "parts": [{"text": "Give a short 5-line summary of today's top tech news."}]
        }]
    }

    response = requests.post(f"{API_URL}?key={API_KEY}", json=payload)

    if response.status_code != 200:
        return f"Gemini API failed: {response.text}"

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
