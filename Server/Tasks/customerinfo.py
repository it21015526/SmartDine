import sqlite3
from datetime import datetime



def init_db():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customerInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            customer_count INTEGER,
            setingExceed INTEGER,
            orderExceed INTEGER,
            FoodExceed INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_customer_info(customer_count, seting_exceed, order_exceed, food_exceed):
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO customerInfo (datetime, customer_count, setingExceed, orderExceed, FoodExceed) 
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), customer_count, seting_exceed, order_exceed, food_exceed))
    conn.commit()
    conn.close()

def get_customer_info():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT datetime, customer_count, setingExceed, orderExceed, FoodExceed 
        FROM customerInfo
        ORDER BY id DESC LIMIT 1
    ''')
    latest_row = cursor.fetchone()
    conn.close()
    return latest_row


