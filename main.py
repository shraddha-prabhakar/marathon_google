from fastapi import FastAPI
import requests
from db import get_db_connection
from email_sender import send_email
from gemini_client import get_summary

app = FastAPI()

@app.post("/subscribe")
def subscribe_user(email: str):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
        conn.commit()
        return {"message": "Subscribed successfully"}
    except:
        return {"message": "Email already subscribed"}
    finally:
        cur.close()
        conn.close()


@app.post("/send")
def send_daily_news():
    # 1. Fetch latest tech news
    url = "https://newsapi.org/v2/top-headlines?category=technology&apiKey=YOUR_NEWSAPI_KEY"
    news = requests.get(url).json()

    articles = [a["title"] for a in news.get("articles", [])[:5]]
    combined = "\n".join(articles)

    # 2. Summarize using Gemini
    summary = get_summary(combined)

    # 3. Get all subscriber emails
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM subscribers")
    subscribers = cur.fetchall()

    # 4. Send email to all
    for row in subscribers:
        email = row[0]
        send_email(email, "Daily Tech News Summary", summary)

    return {"message": "Emails sent successfully"}
