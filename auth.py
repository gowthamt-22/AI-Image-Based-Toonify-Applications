import bcrypt
import re
from email_validator import validate_email, EmailNotValidError
from database import Database

class AuthManager:
    """Handle user authentication and validation"""
    
    def __init__(self):
        self.db = Database()
        self.max_login_attempts = 5
        self.lockout_minutes = 30
    
    def validate_email_format(self, email):
        """Validate email format"""
        try:
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def validate_password_strength(self, password):
        """
        Validate password strength
        Requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character
        """
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
        """
        Validate username
        Requirements:
        - 3-20 characters
        - Only alphanumeric and underscores
        - Must start with letter
        """
        errors = []
        
        if len(username) < 3 or len(username) > 20:
            errors.append("Username must be between 3 and 20 characters")
        
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
            errors.append("Username must start with a letter and contain only letters, numbers, and underscores")
        
        # Check if username already exists
        if self.db.get_user_by_username(username):
            errors.append("Username already taken")
        
        return len(errors) == 0, errors
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def register_user(self, username, email, password, full_name=None):
        """
        Register a new user
        Returns: (success: bool, message: str, user_id: int or None)
        """
        # Validate email
        email_valid, email_result = self.validate_email_format(email)
        if not email_valid:
            return False, f"Invalid email: {email_result}", None
        
        # Check if email already exists
        if self.db.get_user_by_email(email):
            return False, "Email already registered", None
        
        # Validate username
        username_valid, username_errors = self.validate_username(username)
        if not username_valid:
            return False, "; ".join(username_errors), None
        
        # Validate password
        password_valid, password_errors = self.validate_password_strength(password)
        if not password_valid:
            return False, "; ".join(password_errors), None
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user
        user_id = self.db.create_user(username, email, password_hash, full_name)
        
        if user_id:
            return True, "Registration successful", user_id
        else:
            return False, "Registration failed. Please try again.", None
    
    def login_user(self, email, password, ip_address=""):
        """
        Authenticate user login
        Returns: (success: bool, message: str, user_data: dict or None)
        """
        # Check for too many failed attempts
        failed_attempts = self.db.get_failed_login_attempts(email, self.lockout_minutes)
        if failed_attempts >= self.max_login_attempts:
            return False, f"Account temporarily locked due to too many failed attempts. Try again after {self.lockout_minutes} minutes.", None
        
        # Get user by email
        user = self.db.get_user_by_email(email)
        
        if not user:
            self.db.log_login_attempt(email, ip_address, 0)
            return False, "Invalid email or password", None
        
        # Check if account is active
        if not user['is_active']:
            return False, "Account is inactive. Please contact support.", None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            self.db.log_login_attempt(email, ip_address, 0)
            return False, "Invalid email or password", None
        
        # Successful login
        self.db.log_login_attempt(email, ip_address, 1)
        self.db.update_last_login(user['user_id'])
        
        # Remove sensitive data
        user_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'account_type': user['account_type']
        }
        
        return True, "Login successful", user_data
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        user = self.db.get_user_by_id(user_id)
        
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, user['password_hash']):
            return False, "Current password is incorrect"
        
        # Validate new password
        password_valid, password_errors = self.validate_password_strength(new_password)
        if not password_valid:
            return False, "; ".join(password_errors)
        
        # Hash and update new password
        new_hash = self.hash_password(new_password)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ? 
            WHERE user_id = ?
        ''', (new_hash, user_id))
        
        conn.commit()
        conn.close()
        
        return True, "Password changed successfully"
