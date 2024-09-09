import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tableInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            currentturnover INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_table_info(tt_rate):
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tableInfo (datetime, currentturnover) VALUES (?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tt_rate))
    conn.commit()
    conn.close()

def get_table_info():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT datetime, currentturnover FROM tableInfo
        ORDER BY id DESC LIMIT 1
    ''')
    latest_row = cursor.fetchone()
    conn.close()
    return latest_row

save_table_info(4)
