import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls ORDER BY id DESC;")
        urls = cur.fetchall()
    conn.close()
    return urls


def get_url(id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s;", (id,))
        url = cur.fetchone()
    conn.close()
    return url


def get_url_by_name(name):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s;", (name,))
        url = cur.fetchone()
    conn.close()
    return url


def add_url(name):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
            (name,)
        )
        url = cur.fetchone()
        conn.commit()
    conn.close()
    return url['id']
