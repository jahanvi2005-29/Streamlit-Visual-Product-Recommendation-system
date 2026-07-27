"""
Theme management module for the Visual Product Recommendation System.
Ultra-premium design system with mesh gradients, ambient light orbs,
glassmorphism cards, and noise texture — inspired by Vercel, Linear, and Stripe.
"""

import streamlit as st

# ========================================================================
# COLOR SYSTEM — Premium Luxury Palette
# ========================================================================

# Core accent: Electric Indigo (primary), with light/dark variants
ACCENT_INDIGO = "#6366F1"
ACCENT_INDIGO_LIGHT = "#818CF8"
ACCENT_INDIGO_DARK = "#4F46E5"

# Secondary accent values used inline in CSS gradients
ACCENT_CYAN = "#06B6D4"
ACCENT_VIOLET = "#8B5CF6"

# Dark theme — deep slate (#090D16 / #0F172A)
DARK_BG = "#090D16"
DARK_BG_CARD = "rgba(15, 23, 42, 0.65)"
DARK_BG_CARD_SOLID = "#0F172A"
DARK_BG_CARD_HOVER = "rgba(25, 33, 52, 0.8)"
DARK_TEXT = "#F1F5F9"
DARK_TEXT_SECONDARY = "#94A3B8"
DARK_BORDER = "rgba(51, 65, 85, 0.4)"

# Light theme — clean elevated
LIGHT_BG = "#F8FAFC"
LIGHT_BG_CARD = "rgba(255, 255, 255, 0.85)"
LIGHT_BG_CARD_SOLID = "#FFFFFF"
LIGHT_BG_CARD_HOVER = "rgba(255, 255, 255, 0.98)"
LIGHT_TEXT = "#0F172A"
LIGHT_TEXT_SECONDARY = "#64748B"
LIGHT_BORDER = "rgba(203, 213, 225, 0.5)"

# SVG noise texture as data URI — fractal noise, 2% opacity base
NOISE_SVG_BASE64 = (
    "data:image/svg+xml;base64,"
    "PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSczMDAnIGhlaWdodD0nMzAwJz4"
    "8ZmlsdGVyIGlkPSdub2lzZScgeD0nMCcgeT0nMCc+PGZlVHVyYnVsZW5jZSB0eXBlPSdmcmFjdGFsTm9pc2UnI"
    "GJhc2VGcmVxdWVuY3k9JzAuODUnIG51bU9jdGF2ZXM9JzQnIHN0aXRjaFRpbGVzPSdzdGl0Y2gnLz48L2ZpbHR"
    "lcj48cmVjdCB3aWR0aD0nMTAwJScgaGVpZ2h0PScxMDAlJyBmaWx0ZXI9J3VybCgjbm9pc2UpJyBvcGFjaXR5P"
    "ScwLjAyJy8+PC9zdmc+"
)


def init_theme():
    """Initialize the theme in session state if not already set."""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True


def get_theme():
    """Get the current theme colors based on session state."""
    is_dark = st.session_state.get("dark_mode", True)
    if is_dark:
        return {
            "is_dark": True,
            "bg": DARK_BG,
            "card": DARK_BG_CARD_SOLID,
            "card_hover": DARK_BG_CARD_HOVER,
            "text": DARK_TEXT,
            "text_secondary": DARK_TEXT_SECONDARY,
            "border": DARK_BORDER,
            "accent": ACCENT_INDIGO,
            "accent_light": ACCENT_INDIGO_LIGHT,
            "accent_dark": ACCENT_INDIGO_DARK,
            "mode": "dark",
        }
    return {
        "is_dark": False,
        "bg": LIGHT_BG,
        "card": LIGHT_BG_CARD_SOLID,
        "card_hover": LIGHT_BG_CARD_HOVER,
        "text": LIGHT_TEXT,
        "text_secondary": LIGHT_TEXT_SECONDARY,
        "border": LIGHT_BORDER,
        "accent": ACCENT_INDIGO,
        "accent_light": ACCENT_INDIGO_LIGHT,
        "accent_dark": ACCENT_INDIGO_DARK,
        "mode": "light",
    }


def render_theme_toggle():
    """Render the dark/light mode toggle in the sidebar footer."""
    is_dark = st.session_state.get("dark_mode", True)
    icon = "🌙" if is_dark else "☀️"
    label = "Dark Mode" if is_dark else "Light Mode"
    switch_to = "Light" if is_dark else "Dark"

    if st.button(
        f"{icon}  {label}",
        key="theme_toggle_btn",
        help=f"Switch to {switch_to} mode",
        use_container_width=True,
    ):
        st.session_state.dark_mode = not is_dark
        st.rerun()


def get_css():
    """Return the complete premium CSS based on the current theme."""
    is_dark = get_theme()["is_dark"]

    if is_dark:
        return f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}

        /* ===================================================================
                   AMBIENT BACKGROUND SYSTEM
                   Deep slate canvas + noise texture + 4 blurred light orbs (120px blur)
                   Base layer: solid color + noise
                   Orb layer (.stApp::before): 4 Gaussian-blurred orbs with z-index 0
                   =================================================================== */
        .stApp {{
            background: {DARK_BG};
            background-image:
                /* Layer 1: Fractal noise texture at 1% opacity — reduces banding */
                url('{NOISE_SVG_BASE64}'),
                /* Layer 2: Subtle overall warmth radiance */
                radial-gradient(1200px at 50% 30%, rgba(99,102,241,0.03) 0%, transparent 60%);
        }}

        /* 4 ambient light orbs with actual Gaussian blur — safe z-index, behind content */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 0;
            background:
                /* Orb 1 — Electric Indigo, top-right */
                radial-gradient(400px at 80% 10%, rgba(99,102,241,0.18), transparent 60%),
                /* Orb 2 — Cyan, center-left */
                radial-gradient(350px at 15% 50%, rgba(6,182,212,0.12), transparent 60%),
                /* Orb 3 — Violet, bottom */
                radial-gradient(350px at 50% 90%, rgba(139,92,246,0.12), transparent 60%),
                /* Orb 4 — Amber (warmth), bottom-right */
                radial-gradient(300px at 70% 75%, rgba(251,191,36,0.05), transparent 60%);
            filter: blur(110px);
            -webkit-filter: blur(110px);
        }}

        /* ---- Hide Streamlit default UI chrome ---- */
        #MainMenu {{display: none;}}
        footer {{visibility: hidden;}}
        /* Keep header visible — it contains the sidebar reopen arrow */
        header {{visibility: visible !important; height: auto !important; min-height: 0 !important;}}
        header > .stDecoration {{display: none;}}
        div[data-testid=\"stSidebarNav\"] {{display: none !important;}}

        /* ---- Hide native Streamlit sidebar collapse arrow ---- */
        /* The ☰ hamburger (#sbt-btn) is the single sidebar toggle control.    */
        /* We hide the native collapsedControl but keep it in the DOM so the   */
        /* ☰ button's onclick handler can still dispatch a click event on it.  */
        button[data-testid=\"collapsedControl\"] {{
            display: none !important;
        }}

        /* ---- ENTRANCE ANIMATIONS ---- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(18px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }}

        .main .block-container {{
            animation: fadeIn 0.6s ease;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }}

        .metric-card, .custom-card, .hero-section, .section-divider {{
            animation: fadeInUp 0.6s ease both;
        }}

        /* ---- TYPOGRAPHY — Premium SaaS Scale ---- */
        h1, h2, h3, h4, h5, h6, p, li, span, div {{
            color: {DARK_TEXT} !important;
        }}

        h1 {{
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            font-size: 3.2rem !important;
            line-height: 1.15 !important;
        }}

        h2 {{
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
            font-size: 2.2rem !important;
            line-height: 1.25 !important;
        }}

        h3 {{
            font-weight: 600 !important;
            font-size: 1.5rem !important;
            line-height: 1.3 !important;
        }}

        h4 {{ font-weight: 600 !important; font-size: 1.2rem !important; }}

        p, li, .stMarkdown p {{
            font-size: 1.08rem !important;
            line-height: 1.75 !important;
        }}

        strong {{ font-weight: 600; }}

        /* ---- SIDEBAR — Premium Frosted Glass ---- */
        section[data-testid=\"stSidebar\"] {{
            background: rgba(12, 18, 34, 0.85);
            border-right: 1px solid rgba(99, 102, 241, 0.08);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            position: relative;
        }}

        section[data-testid=\"stSidebar\"]::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99,102,241,0.15), transparent);
        }}

        section[data-testid=\"stSidebar\"] .stButton > button {{
            width: 100%;
            text-align: left;
            justify-content: flex-start;
            border: none;
            background: transparent;
            color: {DARK_TEXT_SECONDARY} !important;
            font-weight: 500;
            font-size: 1rem;
            padding: 0.7rem 1.2rem;
            border-radius: 10px;
            transition: all 0.25s ease;
            margin-bottom: 2px;
        }}

        section[data-testid=\"stSidebar\"] .stButton > button:hover {{
            background: rgba(99, 102, 241, 0.1);
            color: {ACCENT_INDIGO} !important;
            transform: translateX(4px);
        }}

        section[data-testid=\"stSidebar\"] .stButton > button[kind=\"primary\"] {{
            background: rgba(99, 102, 241, 0.15) !important;
            color: {ACCENT_INDIGO} !important;
            font-weight: 600;
            border-left: 3px solid {ACCENT_INDIGO};
            border-radius: 10px;
        }}

        section[data-testid=\"stSidebar\"] .stButton > button[kind=\"primary\"]:hover {{
            background: rgba(99, 102, 241, 0.22) !important;
            transform: translateX(4px);
        }}

        section[data-testid=\"stSidebar\"] hr {{
            border-color: rgba(99, 102, 241, 0.07) !important;
            margin: 0.6rem 0 !important;
        }}

        /* ---- PREMIUM FROSTED GLASS CARDS ---- */
        .metric-card {{
            background: {DARK_BG_CARD};
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 1.8rem 1.5rem;
            text-align: center;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 20px 50px -10px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99,102,241,0.25), transparent);
            opacity: 0;
            transition: opacity 0.35s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 28px 60px -12px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255,255,255,0.06);
            border-color: rgba(99, 102, 241, 0.25);
        }}

        .metric-card:hover::before {{ opacity: 1; }}

        .metric-card .metric-value {{
            font-size: 2.4rem;
            font-weight: 800;
            color: {ACCENT_INDIGO} !important;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }}

        .metric-card .metric-label {{
            font-size: 0.9rem;
            color: {DARK_TEXT_SECONDARY} !important;
            margin-top: 0.4rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        .custom-card {{
            background: {DARK_BG_CARD};
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 1.8rem;
            margin-bottom: 1.2rem;
            transition: all 0.3s ease;
            box-shadow: 0 16px 40px -8px rgba(0,0,0,0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }}

        .custom-card:hover {{
            border-color: rgba(99, 102, 241, 0.2);
            box-shadow: 0 20px 50px -10px rgba(99, 102, 241, 0.08);
            transform: translateY(-2px);
        }}

        /* ---- HERO ---- */
        .hero-section {{
            padding: 3.5rem 0 2rem;
            text-align: center;
        }}

        .hero-title {{
            font-size: 3.6rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, {ACCENT_INDIGO}, #EC4899, {ACCENT_VIOLET});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.8rem;
        }}

        .hero-subtitle {{
            font-size: 1.3rem !important;
            color: {DARK_TEXT_SECONDARY} !important;
            font-weight: 400;
            max-width: 750px;
            margin: 0 auto;
            line-height: 1.7;
        }}

        /* ---- FLOW DIAGRAM ---- */
        .flow-box {{
            background: {DARK_BG_CARD};
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            padding: 1.2rem 1.8rem;
            text-align: center;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            min-width: 120px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}

        .flow-box:hover {{
            border-color: {ACCENT_INDIGO};
            box-shadow: 0 12px 32px -8px rgba(99, 102, 241, 0.12);
            transform: translateY(-3px);
        }}

        .flow-arrow {{
            font-size: 1.8rem;
            color: {ACCENT_INDIGO};
            opacity: 0.6;
        }}

        /* ---- BUTTONS ---- */
        .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.5rem 1.2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid {ACCENT_INDIGO};
            background: transparent;
            color: {ACCENT_INDIGO} !important;
        }}

        .stButton > button:hover {{
            background: {ACCENT_INDIGO} !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 12px 32px -8px rgba(99, 102, 241, 0.3);
        }}

        .stButton > button:active {{
            transform: translateY(0);
        }}

        .stButton > button[kind=\"primary\"] {{
            background: {ACCENT_INDIGO} !important;
            color: white !important;
            box-shadow: 0 8px 24px -6px rgba(99, 102, 241, 0.25);
        }}

        .stButton > button[kind=\"primary\"]:hover {{
            background: {ACCENT_INDIGO_LIGHT} !important;
            box-shadow: 0 12px 36px -8px rgba(99, 102, 241, 0.35);
            transform: translateY(-2px);
        }}

        /* ---- SELECT BOX ---- */
        .stSelectbox > div > div {{
            background: {DARK_BG_CARD} !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            font-size: 1rem !important;
            backdrop-filter: blur(8px);
        }}

        .stSelectbox > div > div:hover {{
            border-color: {ACCENT_INDIGO} !important;
        }}

        /* ---- SLIDER ---- */
        .stSlider > div > div > div > div {{ background: {ACCENT_INDIGO} !important; }}
        .stSlider > div > div {{ color: {ACCENT_INDIGO} !important; }}
        .stSlider label {{ font-size: 1rem !important; }}
        .stSlider [data-baseweb=\"slider\"] > div > div {{ background: {ACCENT_INDIGO} !important; }}

        /* ---- TABS ---- */
        .stTabs [data-baseweb=\"tab-list\"] {{
            gap: 0;
            background: {DARK_BG_CARD};
            border-radius: 14px;
            padding: 5px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
        }}

        .stTabs [data-baseweb=\"tab\"] {{
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            font-weight: 500;
            font-size: 1rem;
        }}

        .stTabs [aria-selected=\"true\"] {{
            background: {ACCENT_INDIGO} !important;
            color: white !important;
        }}

        /* ---- BADGES ---- */
        .badge {{ display: inline-block; padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .badge-success {{ background: rgba(16, 185, 129, 0.15); color: #10B981 !important; }}
        .badge-error   {{ background: rgba(239, 68, 68, 0.15); color: #EF4444 !important; }}
        .badge-accent  {{ background: rgba(99, 102, 241, 0.15); color: {ACCENT_INDIGO} !important; }}

        /* ---- SIMILARITY BAR ---- */
        .sim-bar {{ height: 5px; border-radius: 3px; background: rgba(51,65,85,0.5); margin-top: 5px; overflow: hidden; }}
        .sim-bar-fill {{ height: 100%; border-radius: 3px; background: linear-gradient(90deg, {ACCENT_INDIGO}, {ACCENT_INDIGO_LIGHT}); transition: width 0.6s ease; }}

        /* ---- SECTION DIVIDER ---- */
        .section-divider {{
            height: 1px;
            background: linear-gradient(90deg, {ACCENT_INDIGO}, rgba(99,102,241,0.06), transparent);
            margin: 2rem 0;
            border: none;
        }}

        /* ---- ALERTS ---- */
        .stAlert {{ border-radius: 14px; border: none; font-size: 1.05rem !important; padding: 1rem 1.2rem !important; background: {DARK_BG_CARD} !important; }}

        /* ---- CAMERA INPUT ---- */
        .stCameraInput > div {{
            background: {DARK_BG_CARD} !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
            overflow: hidden;
        }}
        .stCameraInput video {{
            border-radius: 14px 14px 0 0;
            background: #000;
        }}
        .stCameraInput button {{
            background: {ACCENT_INDIGO} !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600;
        }}

        /* ---- FILE UPLOADER ---- */
        .stFileUploader > div {{
            background: {DARK_BG_CARD} !important;
            border: 1px dashed rgba(255,255,255,0.12) !important;
            border-radius: 14px !important;
            transition: all 0.3s ease;
        }}
        .stFileUploader > div:hover {{ border-color: {ACCENT_INDIGO} !important; }}

        /* ---- EXPANDER ---- */
        .stExpander {{
            background: {DARK_BG_CARD};
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 14px;
            backdrop-filter: blur(12px);
        }}
        .stExpander summary {{ font-weight: 600; font-size: 1rem; }}

        /* ---- TECH BADGES ---- */
        .tech-badge {{
            display: inline-block;
            padding: 0.5rem 1.1rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            background: rgba(99, 102, 241, 0.08);
            color: {ACCENT_INDIGO} !important;
            border: 1px solid rgba(99, 102, 241, 0.12);
            margin: 0.25rem;
            transition: all 0.3s ease;
        }}
        .tech-badge:hover {{ background: rgba(99, 102, 241, 0.15); transform: translateY(-1px); }}

        /* ---- RESULT ITEMS ---- */
        .result-item {{ text-align: center; transition: all 0.3s ease; }}
        .result-item:hover {{ transform: translateY(-4px); }}
        .result-item .score-label {{ font-size: 0.85rem; color: {DARK_TEXT_SECONDARY} !important; margin-top: 0.4rem; }}
        .result-item .category-tag {{ font-size: 0.8rem; padding: 0.2rem 0.6rem; border-radius: 4px; background: rgba(99,102,241,0.12); color: {ACCENT_INDIGO} !important; }}

        /* ---- SCROLLBAR ---- */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(99,102,241,0.2); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(99,102,241,0.4); }}

        /* ---- IMAGE CONTAINERS ---- */
        .img-container {{ border-radius: 14px; overflow: hidden; border: 2px solid rgba(255,255,255,0.06); transition: all 0.35s ease; }}
        .img-container:hover {{ border-color: {ACCENT_INDIGO}; transform: scale(1.02); box-shadow: 0 16px 40px -8px rgba(99,102,241,0.12); }}

        /* ---- TABLES ---- */
        table {{ font-size: 1rem !important; border-collapse: collapse; }}
        th, td {{ padding: 0.85rem 1.2rem !important; }}
        .stDataFrame, .stTable {{ font-size: 1rem !important; }}

        /* ---- SPINNER ---- */
        .stSpinner > div {{ border-color: {ACCENT_INDIGO} !important; }}

        /* ---- RADIO ---- */
        .stRadio label {{ font-size: 1rem !important; }}

        /* ---- CAPTIONS ---- */
        .stCaption {{ font-size: 0.95rem !important; }}

        /* ---- INFO / WARN / ERROR / SUCCESS ---- */
        .stInfo, .stWarning, .stError, .stSuccess {{ font-size: 1.05rem !important; }}

        /* ---- BEFORE / AFTER COMPARISON SLIDER ---- */
        .comparison-container {{
            max-width: 700px;
            margin: 0 auto 2rem;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .comparison-wrapper {{
            position: relative;
            width: 100%;
            cursor: ew-resize;
            user-select: none;
            -webkit-user-select: none;
            background: #000;
        }}

        .comparison-wrapper img {{
            display: block;
            width: 100%;
            height: auto;
            pointer-events: none;
        }}

        .comparison-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            clip-path: inset(0 50% 0 0);
        }}

        .comparison-overlay img {{
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
        }}

        .comparison-handle {{
            position: absolute;
            top: 0;
            bottom: 0;
            left: 50%;
            width: 3px;
            background: #fff;
            transform: translateX(-50%);
            cursor: ew-resize;
            z-index: 10;
            box-shadow: 0 0 8px rgba(0,0,0,0.6);
            transition: box-shadow 0.2s ease;
        }}

        .comparison-handle:hover {{
            box-shadow: 0 0 16px rgba(99,102,241,0.6);
        }}

        .comparison-handle-drag {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 38px;
            height: 38px;
            background: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.35);
            color: #0F172A;
            transition: all 0.2s ease;
            gap: 2px;
        }}

        .comparison-handle:hover .comparison-handle-drag {{
            transform: translate(-50%, -50%) scale(1.1);
            background: {ACCENT_INDIGO};
            color: white;
        }}

        .comparison-handle-drag-arrow {{
            font-size: 0.7rem;
            opacity: 0.7;
        }}

        .comparison-labels {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.7rem 1.2rem;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(8px);
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        .comparison-label-left {{
            color: #EF4444;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .comparison-label-left::before {{
            content: '✗';
            font-size: 0.9rem;
        }}

        .comparison-label-right {{
            color: #10B981;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .comparison-label-right::after {{
            content: '✓';
            font-size: 0.9rem;
        }}

        .comparison-callout {{
            display: flex;
            gap: 0.75rem;
            align-items: center;
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.15);
            border-radius: 10px;
            padding: 0.6rem 1rem;
            margin-top: 0.5rem;
            font-size: 0.85rem;
        }}

        .comparison-callout-success {{
            background: rgba(16, 185, 129, 0.08);
            border-color: rgba(16, 185, 129, 0.15);
        }}

        /* ---- SIDE-BY-SIDE COMPARE TOGGLE ---- */
        .compare-mode-toggle {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .compare-mode-toggle .toggle-label {{
            font-size: 0.85rem;
            opacity: 0.7;
        }}

        .compare-row {{
            display: flex;
            gap: 1rem;
            align-items: stretch;
            margin-bottom: 1rem;
            padding: 0.75rem;
            background: {DARK_BG_CARD};
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            animation: fadeInUp 0.4s ease both;
        }}

        .compare-row:hover {{
            border-color: rgba(99,102,241,0.25);
            background: {DARK_BG_CARD_HOVER};
            transform: translateX(4px);
        }}

        .compare-side {{
            flex: 1;
            text-align: center;
            min-width: 0;
        }}

        .compare-side img {{
            width: 100%;
            border-radius: 10px;
            display: block;
        }}

        .compare-side-label {{
            font-size: 0.7rem;
            opacity: 0.5;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .compare-vs-divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 44px;
        }}

        .compare-vs-badge {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(99,102,241,0.15);
            border: 1px solid rgba(99,102,241,0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
            color: {ACCENT_INDIGO} !important;
            letter-spacing: 0.02em;
        }}

        .compare-info {{
            margin-top: 0.4rem;
            font-size: 0.85rem;
        }}

        .compare-rank {{
            font-weight: 700;
            color: {ACCENT_INDIGO} !important;
        }}

        /* ---- RESPONSIVE ---- */
        @media (max-width: 768px) {{
            .hero-title {{ font-size: 2.2rem !important; }}
            .hero-subtitle {{ font-size: 1.1rem !important; }}
            h1 {{ font-size: 2.2rem !important; }}
            h2 {{ font-size: 1.6rem !important; }}
            h3 {{ font-size: 1.2rem !important; }}
            .metric-card {{ padding: 1.2rem; }}
            .metric-card .metric-value {{ font-size: 1.8rem; }}
            .compare-row {{ flex-direction: column; }}
            .compare-vs-divider {{ flex: 0 0 auto; padding: 0.3rem 0; }}
            .comparison-handle-drag {{ width: 30px; height: 30px; font-size: 0.8rem; }}
        }}
        </style>"""

    # === LIGHT THEME CSS ===
    return f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}

    /* ===================================================================
               AMBIENT BACKGROUND SYSTEM — Light Mode
               Clean elevated off-white + noise texture + blurred ambient orbs
               =================================================================== */
    .stApp {{
        background: {LIGHT_BG};
        background-image:
            /* Layer 1: Noise texture at 1.5% opacity */
            url('{NOISE_SVG_BASE64}');
    }}

    /* Light mode ambient orbs — lower opacity for bright background */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        z-index: 0;
        background:
            /* Orb 1 — Indigo, top-right */
            radial-gradient(350px at 80% 15%, rgba(99,102,241,0.08), transparent 60%),
            /* Orb 2 — Cyan, center-left */
            radial-gradient(300px at 20% 50%, rgba(6,182,212,0.05), transparent 60%),
            /* Orb 3 — Violet, bottom */
            radial-gradient(300px at 50% 85%, rgba(139,92,246,0.05), transparent 60%),
            /* Orb 4 — Amber (warmth), bottom-right */
            radial-gradient(280px at 70% 75%, rgba(251,191,36,0.03), transparent 60%);
        filter: blur(110px);
        -webkit-filter: blur(110px);
    }}

    /* ---- Hide Streamlit default UI ---- */
    #MainMenu {{display: none;}}
    footer {{visibility: hidden;}}
    /* Keep header visible — it contains the sidebar reopen arrow */
    header {{visibility: visible !important; height: auto !important; min-height: 0 !important;}}
    header > .stDecoration {{display: none;}}
    div[data-testid=\"stSidebarNav\"] {{display: none !important;}}

    /* ---- Hide native Streamlit sidebar collapse arrow ---- */
    /* The ☰ hamburger (#sbt-btn) is the single sidebar toggle control.    */
    /* We hide the native collapsedControl but keep it in the DOM so the   */
    /* ☰ button's onclick handler can still dispatch a click event on it.  */
    button[data-testid=\"collapsedControl\"] {{
        display: none !important;
    }}

    /* ---- ENTRANCE ANIMATIONS ---- */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(18px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}

    .main .block-container {{
        animation: fadeIn 0.6s ease;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }}

    .metric-card, .custom-card, .hero-section, .section-divider {{
        animation: fadeInUp 0.6s ease both;
    }}

    /* ---- TYPOGRAPHY ---- */
    h1, h2, h3, h4, h5, h6, p, li, span, div {{
        color: {LIGHT_TEXT} !important;
    }}

    h1 {{
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        font-size: 3.2rem !important;
        line-height: 1.15 !important;
    }}
    h2 {{
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        font-size: 2.2rem !important;
        line-height: 1.25 !important;
    }}
    h3 {{
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        line-height: 1.3 !important;
    }}
    h4 {{ font-weight: 600 !important; font-size: 1.2rem !important; }}

    p, li, .stMarkdown p {{
        font-size: 1.08rem !important;
        line-height: 1.75 !important;
    }}

    /* ---- SIDEBAR — Premium Frosted Glass ---- */
    section[data-testid=\"stSidebar\"] {{
        background: rgba(255, 255, 255, 0.88);
        border-right: 1px solid rgba(99, 102, 241, 0.06);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
    }}

    section[data-testid=\"stSidebar\"] .stButton > button {{
        width: 100%;
        text-align: left;
        justify-content: flex-start;
        border: none;
        background: transparent;
        color: {LIGHT_TEXT_SECONDARY} !important;
        font-weight: 500;
        font-size: 1rem;
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        transition: all 0.25s ease;
        margin-bottom: 2px;
    }}

    section[data-testid=\"stSidebar\"] .stButton > button:hover {{
        background: rgba(99, 102, 241, 0.06);
        color: {ACCENT_INDIGO} !important;
        transform: translateX(4px);
    }}

    section[data-testid=\"stSidebar\"] .stButton > button[kind=\"primary\"] {{
        background: rgba(99, 102, 241, 0.1) !important;
        color: {ACCENT_INDIGO} !important;
        font-weight: 600;
        border-left: 3px solid {ACCENT_INDIGO};
        border-radius: 10px;
    }}

    section[data-testid=\"stSidebar\"] .stButton > button[kind=\"primary\"]:hover {{
        background: rgba(99, 102, 241, 0.15) !important;
        transform: translateX(4px);
    }}

    section[data-testid=\"stSidebar\"] hr {{
        border-color: rgba(99, 102, 241, 0.06) !important;
        margin: 0.6rem 0 !important;
    }}

    /* ---- PREMIUM FROSTED GLASS CARDS ---- */
    .metric-card {{
        background: {LIGHT_BG_CARD};
        border: 1px solid rgba(203, 213, 225, 0.3);
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 16px 40px -8px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.8);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }}

    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, {ACCENT_INDIGO}, transparent);
        opacity: 0;
        transition: opacity 0.35s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 20px 48px -8px rgba(99, 102, 241, 0.08);
        border-color: rgba(99, 102, 241, 0.2);
    }}

    .metric-card:hover::before {{ opacity: 1; }}

    .metric-card .metric-value {{
        font-size: 2.4rem;
        font-weight: 800;
        color: {ACCENT_INDIGO} !important;
        line-height: 1.1;
    }}

    .metric-card .metric-label {{
        font-size: 0.9rem;
        color: {LIGHT_TEXT_SECONDARY} !important;
        margin-top: 0.4rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    .custom-card {{
        background: {LIGHT_BG_CARD};
        border: 1px solid rgba(203, 213, 225, 0.3);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px -6px rgba(0,0,0,0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }}

    .custom-card:hover {{
        border-color: rgba(99, 102, 241, 0.15);
        box-shadow: 0 16px 40px -8px rgba(99, 102, 241, 0.04);
        transform: translateY(-2px);
    }}

    /* ---- HERO ---- */
    .hero-section {{ padding: 3.5rem 0 2rem; text-align: center; }}

    .hero-title {{
        font-size: 3.6rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, {ACCENT_INDIGO}, #EC4899, {ACCENT_VIOLET});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
    }}

    .hero-subtitle {{
        font-size: 1.3rem !important;
        color: {LIGHT_TEXT_SECONDARY} !important;
        font-weight: 400;
        max-width: 750px;
        margin: 0 auto;
    }}

    /* ---- BUTTONS ---- */
    .stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.5rem 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid {ACCENT_INDIGO};
        background: transparent;
        color: {ACCENT_INDIGO} !important;
    }}

    .stButton > button:hover {{
        background: {ACCENT_INDIGO} !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 32px -8px rgba(99, 102, 241, 0.2);
    }}

    .stButton > button[kind=\"primary\"] {{ background: {ACCENT_INDIGO} !important; color: white !important; box-shadow: 0 8px 24px -6px rgba(99,102,241,0.15); }}
    .stButton > button[kind=\"primary\"]:hover {{ background: {ACCENT_INDIGO_LIGHT} !important; box-shadow: 0 12px 36px -8px rgba(99,102,241,0.25); }}

    /* ---- SELECT BOX ---- */
    .stSelectbox > div > div {{
        background: {LIGHT_BG_CARD} !important;
        border-color: {LIGHT_BORDER} !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        backdrop-filter: blur(8px);
    }}

    /* ---- SLIDER ---- */
    .stSlider > div > div > div > div {{ background: {ACCENT_INDIGO} !important; }}
    .stSlider > div > div {{ color: {ACCENT_INDIGO} !important; }}
    .stSlider label {{ font-size: 1rem !important; }}

    /* ---- TABS ---- */
    .stTabs [data-baseweb=\"tab-list\"] {{
        gap: 0;
        background: {LIGHT_BG_CARD};
        border-radius: 14px;
        padding: 5px;
        border: 1px solid rgba(203, 213, 225, 0.3);
        backdrop-filter: blur(12px);
    }}

    .stTabs [data-baseweb=\"tab\"] {{ border-radius: 10px; padding: 0.6rem 1.2rem; font-weight: 500; font-size: 1rem; }}
    .stTabs [aria-selected=\"true\"] {{ background: {ACCENT_INDIGO} !important; color: white !important; }}

    /* ---- BADGES ---- */
    .badge {{ display: inline-block; padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
    .badge-success {{ background: rgba(16, 185, 129, 0.1); color: #059669 !important; }}
    .badge-error   {{ background: rgba(239, 68, 68, 0.1); color: #DC2626 !important; }}
    .badge-accent  {{ background: rgba(99, 102, 241, 0.1); color: {ACCENT_INDIGO} !important; }}

    /* ---- SIMILARITY BAR ---- */
    .sim-bar {{ height: 5px; border-radius: 3px; background: {LIGHT_BORDER}; margin-top: 5px; overflow: hidden; }}
    .sim-bar-fill {{ height: 100%; border-radius: 3px; background: linear-gradient(90deg, {ACCENT_INDIGO}, {ACCENT_INDIGO_LIGHT}); transition: width 0.6s ease; }}

    /* ---- SECTIONS ---- */
    .section-divider {{ height: 1px; background: linear-gradient(90deg, {ACCENT_INDIGO}, rgba(99,102,241,0.04), transparent); margin: 2rem 0; border: none; }}

    .stAlert {{ border-radius: 14px; border: none; font-size: 1.05rem !important; border: 1px solid rgba(203,213,225,0.3) !important; }}

    .stCameraInput > div {{
        background: {LIGHT_BG_CARD} !important;
        border: 1px solid {LIGHT_BORDER} !important;
        border-radius: 14px !important;
        overflow: hidden;
    }}
    .stCameraInput video {{
        border-radius: 14px 14px 0 0;
        background: #000;
    }}
    .stCameraInput button {{
        background: {ACCENT_INDIGO} !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600;
    }}

    .stFileUploader > div {{ background: {LIGHT_BG_CARD} !important; border: 1px dashed {LIGHT_BORDER} !important; border-radius: 14px !important; }}
    .stFileUploader > div:hover {{ border-color: {ACCENT_INDIGO} !important; }}

    .tech-badge {{ display: inline-block; padding: 0.5rem 1.1rem; border-radius: 10px; font-size: 0.9rem; font-weight: 600; background: rgba(99, 102, 241, 0.06); color: {ACCENT_INDIGO} !important; border: 1px solid rgba(99, 102, 241, 0.1); margin: 0.25rem; transition: all 0.3s ease; }}
    .tech-badge:hover {{ background: rgba(99, 102, 241, 0.1); transform: translateY(-1px); }}

    .flow-box {{ background: {LIGHT_BG_CARD}; border: 1px solid rgba(203,213,225,0.3); border-radius: 14px; padding: 1.2rem 1.8rem; text-align: center; font-weight: 600; font-size: 1rem; transition: all 0.3s ease; backdrop-filter: blur(12px); }}
    .flow-box:hover {{ border-color: {ACCENT_INDIGO}; box-shadow: 0 12px 32px -8px rgba(99,102,241,0.08); transform: translateY(-3px); }}
    .flow-arrow {{ font-size: 1.8rem; color: {ACCENT_INDIGO}; opacity: 0.6; }}

    .result-item {{ text-align: center; transition: all 0.3s ease; }}
    .result-item:hover {{ transform: translateY(-4px); }}
    .result-item .score-label {{ font-size: 0.85rem; color: {LIGHT_TEXT_SECONDARY} !important; margin-top: 0.4rem; }}
    .result-item .category-tag {{ font-size: 0.8rem; padding: 0.2rem 0.6rem; border-radius: 4px; background: rgba(99,102,241,0.08); color: {ACCENT_INDIGO} !important; }}

    .stExpander {{ background: {LIGHT_BG_CARD}; border: 1px solid rgba(203,213,225,0.3); border-radius: 14px; backdrop-filter: blur(12px); }}
    .stExpander summary {{ font-weight: 600; font-size: 1rem; }}

    .stDataFrame > div > div {{ background: {LIGHT_BG_CARD} !important; border-color: {LIGHT_BORDER} !important; }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: {LIGHT_BG}; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(99,102,241,0.15); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(99,102,241,0.3); }}

    .stSpinner > div {{ border-color: {ACCENT_INDIGO} !important; }}
    .stRadio label {{ font-size: 1rem !important; }}
    .stCaption {{ font-size: 0.95rem !important; }}
    .stInfo, .stWarning, .stError, .stSuccess {{ font-size: 1.05rem !important; }}
    .stMarkdown p {{ font-size: 1.05rem !important; }}

    table {{ font-size: 1rem !important; }}
    th, td {{ padding: 0.85rem 1.2rem !important; }}

    .img-container {{ border-radius: 14px; overflow: hidden; border: 2px solid rgba(203,213,225,0.3); transition: all 0.35s ease; }}
    .img-container:hover {{ border-color: {ACCENT_INDIGO}; transform: scale(1.02); box-shadow: 0 16px 40px -8px rgba(99,102,241,0.08); }}

    /* ---- BEFORE / AFTER COMPARISON SLIDER ---- */
    .comparison-container {{
        max-width: 700px;
        margin: 0 auto 2rem;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 20px 50px -10px rgba(0,0,0,0.15);
        border: 1px solid rgba(203, 213, 225, 0.3);
    }}

    .comparison-wrapper {{
        position: relative;
        width: 100%;
        cursor: ew-resize;
        user-select: none;
        -webkit-user-select: none;
        background: #f0f0f0;
    }}

    .comparison-wrapper img {{
        display: block;
        width: 100%;
        height: auto;
        pointer-events: none;
    }}

    .comparison-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        clip-path: inset(0 50% 0 0);
    }}

    .comparison-overlay img {{
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0;
        left: 0;
    }}

    .comparison-handle {{
        position: absolute;
        top: 0;
        bottom: 0;
        left: 50%;
        width: 3px;
        background: #fff;
        transform: translateX(-50%);
        cursor: ew-resize;
        z-index: 10;
        box-shadow: 0 0 8px rgba(0,0,0,0.3);
        transition: box-shadow 0.2s ease;
    }}

    .comparison-handle:hover {{
        box-shadow: 0 0 16px rgba(99,102,241,0.5);
    }}

    .comparison-handle-drag {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 38px;
        height: 38px;
        background: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        color: #0F172A;
        transition: all 0.2s ease;
        gap: 2px;
    }}

    .comparison-handle:hover .comparison-handle-drag {{
        transform: translate(-50%, -50%) scale(1.1);
        background: {ACCENT_INDIGO};
        color: white;
    }}

    .comparison-handle-drag-arrow {{
        font-size: 0.7rem;
        opacity: 0.7;
    }}

    .comparison-labels {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 1.2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(8px);
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }}

    .comparison-label-left {{
        color: #DC2626;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .comparison-label-left::before {{
        content: '✗';
        font-size: 0.9rem;
    }}

    .comparison-label-right {{
        color: #059669;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .comparison-label-right::after {{
        content: '✓';
        font-size: 0.9rem;
    }}

    .comparison-callout {{
        display: flex;
        gap: 0.75rem;
        align-items: center;
        background: rgba(239, 68, 68, 0.06);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-radius: 10px;
        padding: 0.6rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }}

    .comparison-callout-success {{
        background: rgba(16, 185, 129, 0.06);
        border-color: rgba(16, 185, 129, 0.15);
    }}

    /* ---- SIDE-BY-SIDE COMPARE TOGGLE ---- */
    .compare-mode-toggle {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }}

    .compare-mode-toggle .toggle-label {{
        font-size: 0.85rem;
        opacity: 0.7;
    }}

    .compare-row {{
        display: flex;
        gap: 1rem;
        align-items: stretch;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: {LIGHT_BG_CARD};
        border-radius: 14px;
        border: 1px solid rgba(203, 213, 225, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.4s ease both;
    }}

    .compare-row:hover {{
        border-color: rgba(99,102,241,0.2);
        background: {LIGHT_BG_CARD_HOVER};
        transform: translateX(4px);
        box-shadow: 0 8px 24px -6px rgba(99,102,241,0.04);
    }}

    .compare-side {{
        flex: 1;
        text-align: center;
        min-width: 0;
    }}

    .compare-side img {{
        width: 100%;
        border-radius: 10px;
        display: block;
    }}

    .compare-side-label {{
        font-size: 0.7rem;
        opacity: 0.5;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .compare-vs-divider {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 44px;
    }}

    .compare-vs-badge {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: {ACCENT_INDIGO} !important;
        letter-spacing: 0.02em;
    }}

    .compare-info {{
        margin-top: 0.4rem;
        font-size: 0.85rem;
    }}

    .compare-rank {{
        font-weight: 700;
        color: {ACCENT_INDIGO} !important;
    }}

    @media (max-width: 768px) {{
        .hero-title {{ font-size: 2.2rem !important; }}
        h1 {{ font-size: 2.2rem !important; }}
        h2 {{ font-size: 1.6rem !important; }}
        .metric-card .metric-value {{ font-size: 1.8rem; }}
        .compare-row {{ flex-direction: column; }}
        .compare-vs-divider {{ flex: 0 0 auto; padding: 0.3rem 0; }}
        .comparison-handle-drag {{ width: 30px; height: 30px; font-size: 0.8rem; }}
    }}
    </style>"""
