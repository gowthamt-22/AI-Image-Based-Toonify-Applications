# 🚀 Toonify - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Git (for cloning repository)
- Web browser (Chrome, Firefox, Edge)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Infosys project 1"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- streamlit==1.28.0
- opencv-python==4.8.1.78
- Pillow==10.1.0
- numpy==1.24.3
- bcrypt==4.1.1
- email-validator==2.1.0
- python-dotenv==1.0.0
- torch==2.1.0
- torchvision==0.16.0

### 3. Run the Application
```bash
streamlit run landing.py
```

The application will open in your default browser at: **http://localhost:8501**

## First Time Setup

### Create an Account
1. Navigate to http://localhost:8501
2. Click "LOGIN / REGISTER"
3. Go to "REGISTER" tab
4. Fill in details:
   - Username: Your choice (3-20 characters, alphanumeric + underscore)
   - Email: Valid email address
   - Password: Min 8 chars, uppercase, lowercase, digit, special char
   - Confirm Password: Must match
5. Click "Create Account"

### Process Your First Image
1. You'll be redirected to Toonify Studio
2. Click "Upload Your Image" and select an image
3. Choose from 8 cartoon styles:
   - Classic 🎭
   - Smooth 🌊
   - Pencil ✏️
   - Watercolor 🎨
   - Comic 📚
   - Oil Paint 🖼️
   - Pop Art 🌟
   - Anime 🎬
4. Wait for processing (2-5 seconds)
5. View side-by-side comparison

### Make a Payment
1. Click "💳 Pay & Download ($2.99)" button
2. Select payment method (use Credit/Debit Card for testing)
3. Enter test card details:
   - **Card Number**: 4111 1111 1111 1111
   - **Cardholder**: Any name
   - **Expiry**: Any future date (e.g., 12/2026)
   - **CVV**: Any 3 digits (e.g., 123)
4. Click "🔒 Pay $2.99"
5. Wait for processing

### Download Your Image
1. On success page, view transaction details
2. Click "⬇️ Download High-Quality Image"
3. Image will download as PNG (no watermark)
4. You have lifetime access to this image!

## Key Features

### 🎨 Image Processing
- Upload images (JPG, PNG, BMP, WEBP)
- 8 unique cartoon styles
- Real-time processing
- Adjustable parameters (brightness, contrast, saturation, sharpness)
- Side-by-side comparison

### 💳 Payment System
- Multiple payment methods
- Secure transaction processing
- Unique transaction IDs
- Payment verification
- Lifetime download access
- No watermarks on paid images

### 📜 Payment History
- View all transactions
- Transaction details (ID, date, amount, status)
- Summary statistics (total spent, completed count)
- Easy navigation

### 🎨 Themes
- Dark theme (default)
- Light theme
- Toggle button in studio header

## Navigation Guide

### Landing Page (Main Entry)
```
http://localhost:8501/
```
- **LOGIN / REGISTER**: Go to authentication
- View features and examples
- Learn how it works

### Authentication Page
```
http://localhost:8501/auth
```
- **LOGIN Tab**: For existing users
- **REGISTER Tab**: For new users
- **Back to Home**: Return to landing

### Toonify Studio (Main App)
```
http://localhost:8501/toonify_studio
```
- **📜 History**: View payment history
- **🌙/☀️**: Toggle theme
- **🚪 Logout**: Exit application
- Upload and process images
- Pay and download

### Payment Gateway
```
http://localhost:8501/payment
```
- Enter payment details
- Process payment
- View pricing and features

### Payment Success
```
http://localhost:8501/payment_success
```
- View transaction confirmation
- Download purchased image
- Create another or go home

### Payment History
```
http://localhost:8501/payment_history
```
- View all transactions
- See statistics
- Navigate to studio/home

## Testing Scenarios

### Test 1: Complete User Journey
1. ✅ Register new account
2. ✅ Login successfully
3. ✅ Upload image
4. ✅ Apply cartoon style
5. ✅ Make payment
6. ✅ Download image
7. ✅ Check payment history

### Test 2: Payment Verification
1. ✅ Process and pay for an image
2. ✅ Go back to studio
3. ✅ Upload SAME image
4. ✅ Apply SAME style
5. ✅ Verify download available without payment

### Test 3: Multiple Styles
1. ✅ Upload one image
2. ✅ Try different styles
3. ✅ Each style creates unique image ID
4. ✅ Each requires separate payment

### Test 4: Payment Methods
1. ✅ Test Credit/Debit Card
2. ✅ Test PayPal (simulated)
3. ✅ Test Google Pay (simulated)
4. ✅ Test Apple Pay (simulated)

## Troubleshooting

### Issue: Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Stop all Streamlit processes
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

# Wait 2 seconds
Start-Sleep -Seconds 2

# Restart
streamlit run landing.py
```

### Issue: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific module
pip install <module-name>
```

### Issue: Database Locked
**Error**: `database is locked`

**Solution**:
```bash
# Close all other database connections
# Delete the database file (will be recreated)
Remove-Item toonify_users.db
```

### Issue: Image Not Processing
**Problem**: Style button clicked but no result

**Solution**:
- Check image file is valid (JPG, PNG, BMP, WEBP)
- Check file size (< 10MB recommended)
- Refresh the page
- Upload again

### Issue: Payment Not Working
**Problem**: Payment button does nothing

**Solution**:
- Fill in ALL required fields
- Use valid test card: 4111 1111 1111 1111
- Check CVV is 3 digits
- Ensure you're logged in

## Database Management

### View Database
```bash
# Install SQLite browser or use Python
python
>>> import sqlite3
>>> conn = sqlite3.connect('toonify_users.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM users")
>>> print(cursor.fetchall())
>>> cursor.execute("SELECT * FROM payments")
>>> print(cursor.fetchall())
```

### Reset Database
```bash
# Delete database file
Remove-Item toonify_users.db

# Restart application (will create new database)
streamlit run landing.py
```

### Backup Database
```bash
# Copy database file
Copy-Item toonify_users.db toonify_users_backup_$(Get-Date -Format "yyyyMMdd_HHmmss").db
```

## Performance Tips

### For Faster Processing
1. Use images < 2MB
2. Resize large images before upload
3. Close unnecessary browser tabs
4. Clear browser cache if slow

### For Better Results
1. Use high-quality source images
2. Try different styles for different image types
3. Use adjustable parameters for fine-tuning
4. Portrait photos: Smooth, Anime styles work well
5. Landscapes: Watercolor, Oil Paint styles recommended

## Security Notes

### Current Implementation
- Simulated payment gateway (for demonstration)
- SQLite database (local storage)
- bcrypt password hashing
- Email validation
- Session-based authentication

### For Production Deployment
- [ ] Integrate real payment gateway (Stripe/PayPal)
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Implement HTTPS/SSL
- [ ] Add rate limiting
- [ ] Implement CAPTCHA
- [ ] Add two-factor authentication
- [ ] Use environment variables for secrets
- [ ] Implement logging and monitoring

## File Structure
```
Infosys project 1/
├── landing.py                      # Main entry point
├── backend.py                      # Backend logic + payment
├── image_processor.py              # Image transformation
├── transformer_model.py            # CartoonGAN model
├── requirements.txt                # Dependencies
├── PAYMENT_INTEGRATION.md          # Payment docs
├── WEEK_5_6_COMPLETION_REPORT.md  # Project report
├── DEMO_SCRIPT.md                  # Demo guide
├── QUICK_START.md                  # This file
├── toonify_users.db               # SQLite database
└── pages/
    ├── auth.py                     # Login/Register
    ├── toonify_studio.py          # Image processing
    ├── payment.py                  # Payment gateway
    ├── payment_success.py          # Success page
    └── payment_history.py          # Transaction history
```

## Support

### Documentation Files
- **PAYMENT_INTEGRATION.md**: Complete payment system documentation
- **WEEK_5_6_COMPLETION_REPORT.md**: Project completion report
- **DEMO_SCRIPT.md**: Presentation script and demo flow

### Common Commands
```bash
# Start application
streamlit run landing.py

# Stop application
Ctrl + C

# Restart application
Get-Process -Name streamlit | Stop-Process -Force; streamlit run landing.py

# Check Python version
python --version

# Check installed packages
pip list

# Update package
pip install --upgrade <package-name>
```

## Next Steps

1. ✅ Test the complete user flow
2. ✅ Try all 8 cartoon styles
3. ✅ Test payment with different methods
4. ✅ Check payment history
5. ✅ Try theme toggle
6. ✅ Test with different image types

## Contact & Support

For issues or questions:
- Check documentation files
- Review error messages in terminal
- Test with sample images first
- Verify all dependencies installed

---

**Application Status**: ✅ Ready to Use

**Payment System**: ✅ Fully Functional

**Database**: ✅ Automatically Created

**Start Command**: `streamlit run landing.py`

**URL**: http://localhost:8501

---

Happy Toonifying! 🎨✨
