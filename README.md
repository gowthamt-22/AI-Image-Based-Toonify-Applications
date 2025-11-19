# Toonify: The Art of Cartooning Images

## Project Overview
Interactive application that converts real-world images into various cartoon-style effects using OpenCV.

## Week 1-2: User Authentication & Registration System

### Features Implemented
✅ User Registration with validation
✅ User Login and Authentication
✅ Secure Password Management
✅ Database Structure for User Management
✅ Session Management
✅ Input Validation and Error Handling

### Project Structure
```
Infosys project 1/
├── app.py                 # Main Streamlit application
├── auth.py                # Authentication logic and validation
├── database.py            # Database management and operations
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Features

#### 1. User Registration
- Username validation (3-20 characters, alphanumeric + underscore)
- Email validation with proper format checking
- Strong password requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character
- Full name (optional)
- Duplicate email/username prevention

#### 2. User Login
- Email and password authentication
- Account lockout after 5 failed attempts (30 minutes)
- Login attempt tracking for security
- Session management

#### 3. Security Features
- Password hashing using bcrypt
- SQL injection prevention using parameterized queries
- Failed login attempt tracking
- Account lockout mechanism
- Input validation and sanitization

#### 4. User Account Management
- Change password functionality
- User profile information display
- Secure logout

### Database Schema

#### Users Table
- `user_id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `full_name`
- `created_at`
- `last_login`
- `is_active`
- `account_type`

#### User Sessions Table
- `session_id` (Primary Key)
- `user_id` (Foreign Key)
- `session_token`
- `created_at`
- `expires_at`
- `ip_address`

#### Login Attempts Table
- `attempt_id` (Primary Key)
- `email`
- `ip_address`
- `success`
- `attempted_at`

### Testing the System

1. **Registration Test:**
   - Navigate to Sign Up page
   - Enter valid credentials
   - Verify validation errors for:
     - Weak passwords
     - Invalid email formats
     - Short usernames
     - Duplicate usernames/emails

2. **Login Test:**
   - Use registered credentials
   - Test invalid credentials (account lockout after 5 attempts)
   - Verify successful login redirects to main app

3. **Password Change Test:**
   - Login to account
   - Click "Change Password"
   - Verify password strength validation
   - Confirm password update

### Security Considerations

- ✅ Passwords are hashed using bcrypt (never stored in plain text)
- ✅ SQL injection protection via parameterized queries
- ✅ Email validation prevents invalid formats
- ✅ Account lockout prevents brute force attacks
- ✅ Session management for authenticated users
- ✅ Input sanitization and validation

### Future Enhancements (Upcoming Weeks)

- Image upload functionality
- OpenCV cartoon effects implementation
- Edge detection and bilateral filtering
- Color quantization
- Sketch and pencil effects
- Side-by-side image comparison
- User image gallery
- Export processed images

### Dependencies

- `streamlit` - Web application framework
- `opencv-python` - Image processing (for future weeks)
- `Pillow` - Image handling
- `numpy` - Array operations
- `bcrypt` - Password hashing
- `email-validator` - Email format validation
- `python-dotenv` - Environment variable management
- `sqlite3` - Database (built-in with Python)

### Development Notes

- SQLite database file (`toonify_users.db`) will be created automatically on first run
- All passwords are securely hashed before storage
- Session state managed by Streamlit
- Responsive UI design for better user experience

### Contact & Support

For issues or questions, refer to project documentation or contact the development team.

---

**Status:** Week 1-2 Complete ✅
**Next Phase:** Image Processing Features (Weeks 3-4)
