import psycopg2
from config import Config


def get_db_connection():
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    conn.autocommit = False
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id VARCHAR(50) PRIMARY KEY,
            total_score INTEGER NOT NULL DEFAULT 0,
            games_played INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()
