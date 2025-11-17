# main.py
from fastapi import FastAPI
from gemini_client import generate_daily_digest
from email_sender import send_email
from db import list_subscribers, add_subscriber
from pydantic import BaseModel, EmailStr

app = FastAPI()

SYSTEM_INSTRUCTION = """
Write a clean, well-written daily tech update email that feels human, natural, and professional — not like AI.
No greeting, no sign-off. Headlines + 2 sentence summaries. End with Insight of the Day.
"""

USER_PROMPT = """
Tech information includes various topics and trends in AI, software, cybersecurity...
"""

class SubscribeReq(BaseModel):
    email: EmailStr

@app.get("/run-daily")
def run_daily():
    subscribers = list_subscribers()

    content = generate_daily_digest(SYSTEM_INSTRUCTION, USER_PROMPT)

    sent = 0
    for email in subscribers:
        send_email(email, "Your Daily Tech Update", content)
        sent += 1

    return {"status": "success", "sent": sent}

@app.post("/subscribe")
def subscribe(req: SubscribeReq):
    add_subscriber(req.email)
    return {"status": "added", "email": req.email}
