import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tx_hash TEXT,
                amount_usdt REAL,
                amount_khr REAL,
                bank_name TEXT,
                account_number TEXT,
                account_name TEXT,
                screenshot_path TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Exchange rates history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id, username, language='en'):
        self.cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, language)
            VALUES (?, ?, ?)
        ''', (user_id, username, language))
        self.conn.commit()
    
    def get_user_language(self, user_id):
        self.cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 'en'
    
    def set_user_language(self, user_id, language):
        self.cursor.execute('''
            UPDATE users SET language = ? WHERE user_id = ?
        ''', (language, user_id))
        self.conn.commit()
    
    def create_order(self, user_id, tx_hash, amount_usdt, amount_khr, 
                     bank_name, account_number, account_name, screenshot_path=None):
        self.cursor.execute('''
            INSERT INTO orders (user_id, tx_hash, amount_usdt, amount_khr, 
                              bank_name, account_number, account_name, screenshot_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, tx_hash, amount_usdt, amount_khr, 
              bank_name, account_number, account_name, screenshot_path))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_order(self, order_id):
        self.cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        return self.cursor.fetchone()
    
    def get_user_orders(self, user_id):
        self.cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        return self.cursor.fetchall()
    
    def get_pending_orders(self):
        self.cursor.execute('SELECT * FROM orders WHERE status = "pending" ORDER BY created_at ASC')
        return self.cursor.fetchall()
    
    def update_order_status(self, order_id, status):
        self.cursor.execute('''
            UPDATE orders SET status = ?, processed_at = ? WHERE order_id = ?
        ''', (status, datetime.now(), order_id))
        self.conn.commit()
    
    def update_exchange_rate(self, rate):
        self.cursor.execute('INSERT INTO exchange_rates (rate) VALUES (?)', (rate,))
        self.conn.commit()
    
    def get_current_rate(self):
        self.cursor.execute('SELECT rate FROM exchange_rates ORDER BY updated_at DESC LIMIT 1')
        result = self.cursor.fetchone()
        return result[0] if result else 4100
    
    def close(self):
        self.conn.close()

# Global database instance
db = Database()
