import sqlite3
from datetime import datetime



def init_db():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            nonEmpty INTEGER,
            waitingTime INTEGER,
            nonEating INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_interaction_info(nonEmpty, waitingTime, nonEating):
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interInfo (datetime, nonEmpty, waitingTime, nonEating) VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nonEmpty, waitingTime, nonEating))
    conn.commit()
    conn.close()

def get_interaction_info():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT datetime, nonEmpty, waitingTime, nonEating FROM interInfo
        ORDER BY id DESC LIMIT 1
    ''')
    latest_row = cursor.fetchone()
    conn.close()
    return latest_row

def get_all_interaction_info():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM interInfo
    ''')
    all_rows = cursor.fetchall()
    conn.close()
    return all_rows


