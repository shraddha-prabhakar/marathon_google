# db.py
import os
import psycopg2

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")

def get_connection():
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME,
        host=DB_HOST
    )

def list_subscribers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM subscribers;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [r[0] for r in rows]

def add_subscriber(email: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO subscribers (email) VALUES (%s) ON CONFLICT DO NOTHING;", (email,))
        conn.commit()
    finally:
        cur.close()
        conn.close()
