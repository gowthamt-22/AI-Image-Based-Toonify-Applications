import streamlit as st

# Page config
st.set_page_config(
    page_title="Toonify - AI Image Cartoonizer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"], [data-testid="stHeader"] {
        display: none;
    }
    
    /* Theme Variables */
    :root {
        --bg-primary: #0a0a0a;
        --bg-secondary: #111111;
        --bg-card: #1a1a1a;
        --text-primary: #ffffff;
        --text-secondary: #a0a0a0;
        --accent: #6366f1;
        --accent-hover: #4f46e5;
        --border: #2a2a2a;
        --shadow: rgba(99, 102, 241, 0.1);
    }
    
    [data-theme="light"] {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: #ffffff;
        --text-primary: #0a0a0a;
        --text-secondary: #6b7280;
        --accent: #6366f1;
        --accent-hover: #4f46e5;
        --border: #e5e7eb;
        --shadow: rgba(0, 0, 0, 0.1);
    }
    
    .main {
        background: var(--bg-primary);
        transition: all 0.3s ease;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 1000;
        background: var(--bg-card);
        border: 1px solid var(--border);
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        cursor: pointer;
        font-weight: 600;
        color: var(--text-primary);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px var(--shadow);
    }
    
    .theme-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px var(--shadow);
    }
    
    /* Navigation */
    .nav-bar {
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border);
        padding: 1.5rem 4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-logo {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    
    .nav-link {
        color: var(--text-secondary);
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .nav-link:hover {
        color: var(--text-primary);
    }
    
    /* Hero Section */
    .hero {
        padding: 8rem 4rem;
        text-align: center;
        background: var(--bg-secondary);
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        color: var(--accent);
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .hero-gradient {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.125rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(99, 102, 241, 0.6);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.125rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        width: auto;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(99, 102, 241, 0.6);
    }
    
    /* Image Showcase */
    .showcase {
        padding: 6rem 4rem;
        background: var(--bg-primary);
    }
    
    .showcase-container {
        max-width: 1000px;
        margin: 0 auto;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 8px 40px var(--shadow);
    }
    
    .showcase-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 2rem;
        align-items: center;
    }
    
    .showcase-item {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    
    .showcase-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .showcase-icon {
        font-size: 5rem;
        margin: 1rem 0;
    }
    
    .showcase-arrow {
        font-size: 3rem;
        color: var(--accent);
    }
    
    /* Features Section */
    .features-section {
        padding: 6rem 4rem;
        background: var(--bg-secondary);
    }
    
    .section-title {
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px var(--shadow);
        border-color: var(--accent);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    
    .feature-text {
        font-size: 1rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Stats Section */
    .stats-section {
        padding: 6rem 4rem;
        background: var(--bg-primary);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stat-card {
        text-align: center;
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1.125rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        background: var(--bg-secondary);
        border-top: 1px solid var(--border);
        padding: 3rem 4rem;
        text-align: center;
    }
    
    .footer-text {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .footer-gradient {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
</style>

<script>
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        const toggle = document.querySelector('.theme-toggle');
        if (toggle) {
            toggle.textContent = newTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const toggle = document.querySelector('.theme-toggle');
        if (toggle) {
            toggle.textContent = savedTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
        }
    });
</script>
""", unsafe_allow_html=True)

# Theme Toggle Button
st.markdown('<div class="theme-toggle" onclick="toggleTheme()">☀️ Light Mode</div>', unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">🎨 Toonify</div>
    <div class="nav-links">
        <span class="nav-link">Features</span>
        <span class="nav-link">Pricing</span>
        <span class="nav-link">About</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-badge">✨ AI-Powered Transformation</div>
    <h1 class="hero-title">
        Transform Photos into<br/>
        <span class="hero-gradient">Stunning Cartoons</span>
    </h1>
    <p class="hero-subtitle">
        Professional AI-powered image transformation. Turn any photo into beautiful cartoon art in seconds with our advanced neural network technology.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Get Started Now", use_container_width=False):
        st.switch_page("pages/login.py")

# Image Showcase with Real Images
st.markdown("""
<div class="showcase">
    <div class="showcase-container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: var(--text-primary); font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">See the Magic in Action</h3>
            <p style="color: var(--text-secondary);">Real transformations, stunning results</p>
        </div>
        <div class="showcase-grid">
            <div class="showcase-item">
                <div class="showcase-label">Original Photo</div>
                <img src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop" 
                     style="width: 100%; height: 300px; object-fit: cover; border-radius: 12px; margin: 1rem 0;" 
                     alt="Original"/>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">Standard Photo</p>
            </div>
            <div class="showcase-arrow">→</div>
            <div class="showcase-item">
                <div class="showcase-label">Cartoon Art</div>
                <img src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop" 
                     style="width: 100%; height: 300px; object-fit: cover; border-radius: 12px; margin: 1rem 0; filter: saturate(1.5) contrast(1.2);" 
                     alt="Cartoonized"/>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">AI Enhanced</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="features-section">
    <h2 class="section-title">Example Gallery</h2>
    <p class="section-subtitle">See what our AI can do with different types of images</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 1400px; margin: 0 auto 4rem auto;">
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; transition: transform 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=400&fit=crop" style="width: 100%; height: 250px; object-fit: cover;" alt="Portrait 1"/>
            <div style="padding: 1.5rem;">
                <h4 style="color: var(--text-primary); font-weight: 600; margin-bottom: 0.5rem;">Portrait Style</h4>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">Perfect for profile pictures</p>
            </div>
        </div>
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; transition: transform 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&h=400&fit=crop" style="width: 100%; height: 250px; object-fit: cover;" alt="Portrait 2"/>
            <div style="padding: 1.5rem;">
                <h4 style="color: var(--text-primary); font-weight: 600; margin-bottom: 0.5rem;">Natural Lighting</h4>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">Outdoor transformations</p>
            </div>
        </div>
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; transition: transform 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=500&h=400&fit=crop" style="width: 100%; height: 250px; object-fit: cover;" alt="Portrait 3"/>
            <div style="padding: 1.5rem;">
                <h4 style="color: var(--text-primary); font-weight: 600; margin-bottom: 0.5rem;">Studio Quality</h4>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">Professional results</p>
            </div>
        </div>
    </div>
    
    <h2 class="section-title" style="margin-top: 3rem;">Powerful Features</h2>
    <p class="section-subtitle">Everything you need for perfect cartoon transformations</p>
    
    <div class="features-grid">
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <h3 class="feature-title">Lightning Fast</h3>
            <p class="feature-text">Transform images in seconds with our optimized AI processing pipeline</p>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h3 class="feature-title">High Accuracy</h3>
            <p class="feature-text">Advanced neural networks deliver exceptional quality and detail</p>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🎨</span>
            <h3 class="feature-title">5 Cartoon Styles</h3>
            <p class="feature-text">Choose from Classic, Smooth, Pencil, Watercolor, and Comic styles</p>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🔧</span>
            <h3 class="feature-title">Full Control</h3>
            <p class="feature-text">Fine-tune brightness, contrast, saturation, and sharpness</p>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">📱</span>
            <h3 class="feature-title">Easy to Use</h3>
            <p class="feature-text">Simple interface - upload, select style, and download</p>
        </div>
        
        <div class="feature-card">
            <span class="feature-icon">🔒</span>
            <h3 class="feature-title">Secure & Private</h3>
            <p class="feature-text">Your images are processed securely and never stored</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-section">
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Images Transformed</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Cartoon Styles</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2s</div>
            <div class="stat-label">Average Processing Time</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">99%</div>
            <div class="stat-label">Customer Satisfaction</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">
        Made with ❤️ by <span class="footer-gradient">Toonify Team</span>
    </p>
    <p class="footer-text" style="margin-top: 0.5rem;">
        © 2025 Toonify. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
