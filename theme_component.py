"""
Reusable theme toggle component for all pages
"""

def get_theme_css():
    """Returns CSS variables for theme support"""
    return """
    <style>
        /* Theme Variables */
        :root {
            --bg-primary: #0f0c29;
            --bg-secondary: #302b63;
            --bg-tertiary: #24243e;
            --text-primary: #a8b2d1;
            --text-secondary: #8892b0;
            --border-color: rgba(102, 126, 234, 0.3);
            --glow-color: rgba(102, 126, 234, 0.5);
        }
        
        [data-theme="light"] {
            --bg-primary: #f5f7fa;
            --bg-secondary: #ffffff;
            --bg-tertiary: #e5e7eb;
            --text-primary: #1f2937;
            --text-secondary: #4b5563;
            --border-color: rgba(102, 126, 234, 0.4);
            --glow-color: rgba(102, 126, 234, 0.6);
        }
        
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 0.6rem 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .theme-toggle:hover {
            box-shadow: 0 0 30px var(--glow-color);
            transform: scale(1.05);
        }
    </style>
    """

def get_theme_script():
    """Returns JavaScript for theme switching"""
    return """
    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            const btn = document.querySelector('.theme-toggle');
            if (btn) {
                btn.innerHTML = newTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
            const btn = document.querySelector('.theme-toggle');
            if (btn) {
                btn.innerHTML = savedTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
            }
        });
    </script>
    """

def get_theme_toggle_button():
    """Returns HTML for theme toggle button"""
    return '<div class="theme-toggle" onclick="toggleTheme()">☀️ Light Mode</div>'

def get_hero_svg():
    """Returns SVG illustration for hero section"""
    return """
    <svg width="100%" height="400" viewBox="0 0 800 400" style="border-radius: 15px;">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <rect width="800" height="400" fill="url(#grad1)" opacity="0.15"/>
        
        <!-- Decorative circles -->
        <circle cx="150" cy="100" r="40" fill="#667eea" opacity="0.4" filter="url(#glow)"/>
        <circle cx="680" cy="320" r="60" fill="#764ba2" opacity="0.4" filter="url(#glow)"/>
        <circle cx="700" cy="80" r="30" fill="#667eea" opacity="0.3"/>
        
        <!-- Main frame -->
        <rect x="200" y="80" width="400" height="240" rx="20" fill="rgba(255,255,255,0.05)" stroke="#667eea" stroke-width="3"/>
        
        <!-- Split screen effect (Before/After) -->
        <rect x="210" y="90" width="180" height="220" rx="15" fill="rgba(102, 126, 234, 0.2)"/>
        <rect x="400" y="90" width="190" height="220" rx="15" fill="rgba(118, 75, 162, 0.2)"/>
        
        <!-- Arrow icon -->
        <path d="M 380 190 L 410 190 L 410 180 L 430 200 L 410 220 L 410 210 L 380 210 Z" fill="#ffffff" opacity="0.8"/>
        
        <!-- Cartoon emoji and text -->
        <text x="300" y="210" font-size="64" text-anchor="middle">📷</text>
        <text x="495" y="210" font-size="64" text-anchor="middle">🎨</text>
        
        <!-- Labels -->
        <text x="300" y="280" font-size="16" fill="#ffffff" text-anchor="middle" opacity="0.9">Original</text>
        <text x="495" y="280" font-size="16" fill="#ffffff" text-anchor="middle" opacity="0.9">Cartoonized</text>
        
        <!-- Title -->
        <text x="400" y="50" font-size="28" fill="#ffffff" text-anchor="middle" font-weight="bold">AI-Powered Transformation</text>
    </svg>
    """
