import sqlite3
import os
from datetime import datetime

class Database:
    """Database handler for user authentication and management"""
    
    def __init__(self, db_name='toonify_users.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                account_type TEXT DEFAULT 'user'
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Login attempts table (for security tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                ip_address TEXT,
                success INTEGER DEFAULT 0,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password_hash, full_name=None):
        """Create a new user in the database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError as e:
            return None
    
    def get_user_by_email(self, email):
        """Retrieve user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def get_user_by_username(self, username):
        """Retrieve user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def get_user_by_id(self, user_id):
        """Retrieve user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def update_last_login(self, user_id):
        """Update user's last login timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def log_login_attempt(self, email, ip_address, success):
        """Log login attempt for security tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO login_attempts (email, ip_address, success)
            VALUES (?, ?, ?)
        ''', (email, ip_address, success))
        
        conn.commit()
        conn.close()
    
    def get_failed_login_attempts(self, email, minutes=30):
        """Get number of failed login attempts in last N minutes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM login_attempts 
            WHERE email = ? 
            AND success = 0 
            AND attempted_at > datetime('now', '-' || ? || ' minutes')
        ''', (email, minutes))
        
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] if result else 0
