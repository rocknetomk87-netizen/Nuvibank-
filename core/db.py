import sqlite3
from config.settings import Config

def get_db_connection():
    db_path = Config.DATABASE_URL.replace("sqlite:///", "")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn
