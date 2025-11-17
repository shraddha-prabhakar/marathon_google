# gemini_client.py
import requests
import google.auth
import google.auth.transport.requests

MODEL_NAME = "models/gemini-2.5-flash"
BASE_URL = "https://generative.googleapis.com/v1beta2"

def get_token():
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token

def generate_daily_digest(system_instruction, user_message):
    token = get_token()
    url = f"{BASE_URL}/{MODEL_NAME}:generateText"
    payload = {
        "prompt": {
            "messages": [
                {"author": "system", "content": [{"type": "text", "text": system_instruction}]},
                {"author": "user", "content": [{"type": "text", "text": user_message}]}
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers, timeout=60)
    res.raise_for_status()
    data = res.json()

    if "candidates" in data:
        return data["candidates"][0]["content"]
    return str(data)
