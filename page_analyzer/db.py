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
        cur.execute("""
            SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                urls.created_at,
                url_checks.created_at as last_check_date,
                url_checks.status_code as last_status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.id DESC;
        """)
        urls = cur.fetchall()
    conn.close()
    return urls


def add_url_check(url_id, status_code=None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s) RETURNING id;",
            (url_id, status_code)
        )
        check = cur.fetchone()
        conn.commit()
    conn.close()
    return check['id']


def get_url_checks(url_id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;",
            (url_id,)
        )
        checks = cur.fetchall()
    conn.close()
    return checks


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
