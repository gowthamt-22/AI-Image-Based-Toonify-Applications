import bcrypt
import re
import sqlite3
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

class Backend:
    """Backend handler for user authentication"""
    
    def __init__(self, db_name='toonify_users.db'):
        self.db_name = db_name
        self.max_login_attempts = 5
        self.lockout_minutes = 30
        self.init_database()
        self.init_payment_tables()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
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
                age INTEGER,
                mobile_no TEXT,
                gender TEXT,
                location TEXT,
                city TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                account_type TEXT DEFAULT 'user'
            )
        ''')
        
        # Login attempts table
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
    
    def validate_email_format(self, email):
        """Validate email format"""
        try:
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def validate_username(self, username):
        """Validate username"""
        errors = []
        
        if len(username) < 3 or len(username) > 20:
            errors.append("Username must be between 3 and 20 characters")
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
            errors.append("Username must start with a letter and contain only letters, numbers, and underscores")
        
        # Check if username exists
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            errors.append("Username already taken")
        conn.close()
        
        return len(errors) == 0, errors
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def validate_mobile(self, mobile):
        """Validate mobile number"""
        if not mobile:
            return True, []
        
        errors = []
        # Remove spaces and dashes
        mobile_clean = mobile.replace(" ", "").replace("-", "")
        
        if not mobile_clean.isdigit():
            errors.append("Mobile number must contain only digits")
        elif len(mobile_clean) != 10:
            errors.append("Mobile number must be 10 digits")
        
        return len(errors) == 0, errors
    
    def register_user(self, username, email, password, full_name=None, age=None, mobile_no=None, gender=None, location=None, city=None):
        """Register a new user"""
        # Validate email
        email_valid, email_result = self.validate_email_format(email)
        if not email_valid:
            return False, f"Invalid email: {email_result}", None
        
        # Check if email exists
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered", None
        conn.close()
        
        # Validate username
        username_valid, username_errors = self.validate_username(username)
        if not username_valid:
            return False, "; ".join(username_errors), None
        
        # Validate password
        password_valid, password_errors = self.validate_password_strength(password)
        if not password_valid:
            return False, "; ".join(password_errors), None
        
        # Validate age
        if age and (age < 13 or age > 120):
            return False, "Age must be between 13 and 120", None
        
        # Validate mobile
        if mobile_no:
            mobile_valid, mobile_errors = self.validate_mobile(mobile_no)
            if not mobile_valid:
                return False, "; ".join(mobile_errors), None
        
        # Hash password and create user
        password_hash = self.hash_password(password)
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, age, mobile_no, gender, location, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, age, mobile_no, gender, location, city))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, "Registration successful", user_id
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}", None
    
    def login_user(self, email, password, ip_address=""):
        """Authenticate user login"""
        # Check failed attempts
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM login_attempts 
            WHERE email = ? 
            AND success = 0 
            AND attempted_at > datetime('now', '-' || ? || ' minutes')
        ''', (email, self.lockout_minutes))
        result = cursor.fetchone()
        failed_attempts = result['count'] if result else 0
        
        if failed_attempts >= self.max_login_attempts:
            conn.close()
            return False, f"Account locked. Too many failed attempts. Try again after {self.lockout_minutes} minutes.", None
        
        # Get user
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if not user:
            # Log failed attempt
            cursor.execute('''
                INSERT INTO login_attempts (email, ip_address, success)
                VALUES (?, ?, 0)
            ''', (email, ip_address))
            conn.commit()
            conn.close()
            return False, "Invalid email or password", None
        
        # Check if active
        if not user['is_active']:
            conn.close()
            return False, "Account is inactive", None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            # Log failed attempt
            cursor.execute('''
                INSERT INTO login_attempts (email, ip_address, success)
                VALUES (?, ?, 0)
            ''', (email, ip_address))
            conn.commit()
            conn.close()
            return False, "Invalid email or password", None
        
        # Successful login
        cursor.execute('''
            INSERT INTO login_attempts (email, ip_address, success)
            VALUES (?, ?, 1)
        ''', (email, ip_address))
        cursor.execute('''
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE user_id = ?
        ''', (user['user_id'],))
        conn.commit()
        conn.close()
        
        # Return user data
        user_dict = dict(user)
        user_data = {
            'user_id': user_dict['user_id'],
            'username': user_dict['username'],
            'email': user_dict['email'],
            'full_name': user_dict.get('full_name'),
            'age': user_dict.get('age'),
            'mobile_no': user_dict.get('mobile_no'),
            'gender': user_dict.get('gender'),
            'location': user_dict.get('location'),
            'city': user_dict.get('city'),
            'account_type': user_dict.get('account_type', 'user')
        }
        
        return True, "Login successful", user_data
    
    def init_payment_tables(self):
        """Initialize payment-related database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                payment_method TEXT,
                transaction_id TEXT UNIQUE,
                payment_status TEXT DEFAULT 'pending',
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Downloaded images table (track what users have paid for)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_downloads (
                download_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_id TEXT NOT NULL,
                payment_id INTEGER NOT NULL,
                download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_payment(self, user_id, image_id, amount, payment_method='card'):
        """Create a new payment record"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Generate transaction ID
            import uuid
            transaction_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"
            
            cursor.execute('''
                INSERT INTO payments (user_id, image_id, amount, payment_method, transaction_id, payment_status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            ''', (user_id, image_id, amount, payment_method, transaction_id))
            
            payment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Payment initiated", {'payment_id': payment_id, 'transaction_id': transaction_id}
        except Exception as e:
            return False, f"Payment creation failed: {str(e)}", None
    
    def process_payment(self, payment_id, transaction_id):
        """Process and confirm payment (simulate payment gateway)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Update payment status
            cursor.execute('''
                UPDATE payments 
                SET payment_status = 'completed'
                WHERE payment_id = ? AND transaction_id = ?
            ''', (payment_id, transaction_id))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Payment not found"
            
            conn.commit()
            conn.close()
            
            return True, "Payment processed successfully"
        except Exception as e:
            return False, f"Payment processing failed: {str(e)}"
    
    def verify_payment(self, user_id, image_id):
        """Verify if user has paid for this image"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT payment_id, transaction_id, payment_status 
            FROM payments 
            WHERE user_id = ? AND image_id = ? AND payment_status = 'completed'
            ORDER BY payment_date DESC
            LIMIT 1
        ''', (user_id, image_id))
        
        payment = cursor.fetchone()
        conn.close()
        
        if payment:
            return True, dict(payment)
        return False, None
    
    def record_download(self, user_id, image_id, payment_id):
        """Record that user downloaded the image"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_downloads (user_id, image_id, payment_id)
                VALUES (?, ?, ?)
            ''', (user_id, image_id, payment_id))
            
            conn.commit()
            conn.close()
            
            return True, "Download recorded"
        except Exception as e:
            return False, f"Failed to record download: {str(e)}"
    
    def get_user_payment_history(self, user_id):
        """Get payment history for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT payment_id, image_id, amount, currency, payment_method, 
                   transaction_id, payment_status, payment_date
            FROM payments 
            WHERE user_id = ?
            ORDER BY payment_date DESC
        ''', (user_id,))
        
        payments = cursor.fetchall()
        conn.close()
        
        return [dict(payment) for payment in payments]
