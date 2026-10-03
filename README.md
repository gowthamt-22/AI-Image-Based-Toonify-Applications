# Toonify: The Art of Cartooning Images 🎨

## Project Overview
Toonify Studio is an interactive, premium web application that converts real-world images into stunning cartoon-style effects using OpenCV and AI. Featuring a state-of-the-art glassmorphism UI, real-time image enhancements, and a fully functional mock payment gateway.

## ✨ Key Features (Fully Implemented)

### 1. 🎨 Stunning UI/UX Design System
- **Premium Glassmorphism Aesthetics:** Frosted-glass cards, translucent layers, and a vibrant Purple-to-Cyan gradient background.
- **7-Screen User Journey:** A seamless flow from the Landing Page to Auth, Dashboard, Fine-Tuning, Preview, Checkout, and Success.
- **Responsive & Dynamic:** Glowing buttons, micro-animations, and styled file dropzones.

### 2. 🤖 Advanced Image Processing & Filters
- **8 Unique AI Styles:** Classic, Pencil Sketch, Watercolor, Comic, Oil Paint, Pop Art, Anime, and Cartoon.
- **Fine-Tune Parameters:** Real-time adjustable sliders for **Brightness**, **Contrast**, **Saturation**, and **Sharpness** (powered by PIL `ImageEnhance`).
- **OpenCV Integration:** High-performance image processing using `cv2.bilateralFilter`, edge detection, color quantization, and more.

### 3. 💳 Secure Payment Gateway (Checkout Flow)
- **Interactive Checkout:** A gorgeous glassmorphism checkout modal displaying the selected filter, price (₹99.00), and feature list.
- **Payment Methods:** Support for Credit/Debit Card, PayPal, Google Pay, and Apple Pay mock selection.
- **Success Receipt:** Generates a unique Transaction ID and a beautiful success receipt before allowing the high-res image download.

### 4. 🔒 User Authentication & Security
- User Registration and Login with session state management.
- Secure password handling, bcrypt hashing, and input validation.

## 🛠️ Project Structure
```text
Infosys project/
├── app.py                 # Main Streamlit application (Frontend + UI Logic + Payment)
├── filters/               # Directory containing OpenCV filter modules
│   ├── cartoon_filter.py
│   ├── sketch_filter.py
│   └── pencil_filter.py
├── auth.py                # Authentication logic and validation
├── database.py            # Database management and operations
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## 🚀 Installation & Running

1. **Clone the repository:**
```bash
git clone https://github.com/gowthamt-22/AI-Image-Based-Toonify-Applications.git
cd AI-Image-Based-Toonify-Applications
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
# Alternatively, ensure these are installed:
pip install streamlit opencv-python Pillow numpy bcrypt email-validator python-dotenv
```

3. **Run the Application:**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📸 Workflow Guide
1. **Home/Landing:** View features and metrics. Click "Login" or "Register".
2. **Dashboard:** Drag & drop your image into the styled uploader.
3. **Style Selection:** Choose from 8 premium filters.
4. **Fine-Tuning:** Adjust image parameters and preview the side-by-side transformation.
5. **Checkout:** Proceed to the mock secure payment gateway for ₹99.00.
6. **Download:** Receive your transaction receipt and download the final high-res `.png` result!

---

**Status:** Project Complete ✅
**Technologies:** Python, Streamlit, OpenCV, PIL, HTML/CSS
