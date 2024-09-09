import sqlite3
from datetime import datetime




def init_db():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tableInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            rearrangingTime INTEGER,
            CleaningTime INTEGER,
            ttrate float
        )
    ''')
    conn.commit()
    conn.close()

def save_table_info(rearrangingTime, cleaningTime, tt_rate):
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tableInfo (datetime, rearrangingTime, CleaningTime, ttrate)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rearrangingTime, cleaningTime, tt_rate))
    conn.commit()
    conn.close()


def get_table_info():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    
    # Get today's date in the format YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT 
            AVG(rearrangingTime) AS avg_rearrangingTime,
            SUM(rearrangingTime) AS sum_rearrangingTime,
            AVG(CleaningTime) AS avg_cleaningTime,
            SUM(CleaningTime) AS sum_cleaningTime,
            ttrate,
            datetime as datetime
        FROM tableInfo
        WHERE DATE(datetime) = ?
        group by datetime
    ''', (today,))
    
    latest_row = cursor.fetchone()
    conn.close()
    return latest_row



save_table_info(280, 88, 3.1)

