from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from db import get_db_connection
from email_sender import send_email
from gemini_client import get_daily_tech_news

app = FastAPI()

# ---------- MODELS ----------
class SubscribeRequest(BaseModel):
    email: EmailStr

# ---------- ROOT + HEALTH ----------
@app.get("/")
def root():
    return {"status": "DailyTech API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- SUBSCRIBE ----------
@app.post("/subscribe")
def subscribe(request: SubscribeRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (email) VALUES (%s) ON CONFLICT DO NOTHING",
            (request.email,)
        )
        conn.commit()
        return {"message": f"Subscribed: {request.email}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# ---------- SEND NEWSLETTER ----------
@app.post("/send-newsletter")
def send_newsletter():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch all subscribers
        cursor.execute("SELECT email FROM subscribers")
        subscribers = [row[0] for row in cursor.fetchall()]

        if not subscribers:
            return {"message": "No subscribers yet!"}

        # Get AI generated news
        news_content = get_daily_tech_news()

        # Send emails
        for email in subscribers:
            send_email(email, "Your Daily Tech Update", news_content)

        return {"message": f"Newsletter sent to {len(subscribers)} subscribers"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
