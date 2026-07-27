"""
Visual Product Recommendation System — Streamlit Multi-Page Application
Author: Jahanvi Gupta
Built with: Streamlit, TensorFlow/Keras, scikit-learn, Plotly, NumPy
"""

import streamlit as st
from utils.components import run_parent_script
from utils.theme import init_theme, get_css, render_theme_toggle

# Page config — MUST be the very first Streamlit command
st.set_page_config(
    page_title="Visual Product Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit's default auto-generated sidebar page selector (v1.35+)
try:
    st.set_option('client.showSidebarNavigation', False)
except Exception:
    pass  # Older Streamlit versions don't support this option

# Initialize theme in session state
init_theme()
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

# Inject custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

# ---- Sidebar toggle button: HTML + CSS via st.markdown ----
# The button markup and styles render correctly in st.markdown.
# The JavaScript (onclick handler, MutationObserver) is in a separate
# components.v1.html() call below, because Streamlit 1.60.0 strips inline
# event handlers and <script> tags from st.markdown output.
st.markdown(
    """
    <button id="sbt-btn" title="Toggle sidebar" aria-label="Toggle sidebar">
        ☰
    </button>
    <style>
    #sbt-btn {
        position: fixed; top: 14px; left: 12px; z-index: 9999999;
        display: flex; align-items: center; justify-content: center;
        width: 40px; height: 40px; border-radius: 12px;
        border: 1px solid rgba(99,102,241,0.2);
        background: rgba(99,102,241,0.12);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        color: #818CF8; font-size: 1.2rem; cursor: pointer;
        transition: all 0.25s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        padding: 0;
        line-height: 1;
        outline: none;
    }
    /* Default state: sidebar is open — button is subtle */
    #sbt-btn:not(.sb-collapsed) {
        opacity: 0.55;
    }
    #sbt-btn:not(.sb-collapsed):hover {
        opacity: 1;
    }
    /* Collapsed state: sidebar is hidden — button is prominent */
    #sbt-btn.sb-collapsed {
        opacity: 1;
        background: rgba(99,102,241,0.22);
        border-color: rgba(99,102,241,0.35);
        box-shadow: 0 4px 20px rgba(99,102,241,0.2);
    }
    /* Unknown state: can't find sidebar — always fully visible */
    #sbt-btn.sb-unknown {
        opacity: 1;
        background: rgba(239,68,68,0.15);
        border-color: rgba(239,68,68,0.3);
    }
    #sbt-btn:hover {
        background: rgba(99,102,241,0.28);
        border-color: rgba(99,102,241,0.4);
        transform: scale(1.12);
        box-shadow: 0 8px 24px rgba(99,102,241,0.25);
    }
    /* When collapsed, hover is even more prominent */
    #sbt-btn.sb-collapsed:hover {
        background: rgba(99,102,241,0.35);
        border-color: rgba(99,102,241,0.5);
        transform: scale(1.15);
        box-shadow: 0 8px 28px rgba(99,102,241,0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Sidebar toggle JS: injected via run_parent_script() ----
# run_parent_script() uses components.v1.html internally to execute JS
# in a real iframe context where Streamlit's markdown sanitizer cannot
# strip it. The ``doc`` variable is pre-declared as
# window.parent.document, so the code below can access the main page DOM.
run_parent_script('''
    var btn = doc.getElementById('sbt-btn');
    if (!btn) return;

    // ---- Single toggle for sidebar open/close ----
    // The native collapsedControl is hidden via CSS (display:none) but still
    // exists in the DOM. We dispatch a click event on it programmatically;
    // the event bubbles up to React's event delegation and triggers
    // Streamlit's internal sidebar toggle mechanism.
    btn.onclick = function() {
        var cc = doc.querySelector('[data-testid="collapsedControl"]');
        if (cc) {
            cc.dispatchEvent(new MouseEvent('click', {
                bubbles: true,
                cancelable: true
            }));
            return;
        }
        // Fallback: dispatch click on the sidebar toggle header button
        var sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            var innerBtn = sidebar.querySelector('button');
            if (innerBtn) innerBtn.click();
        }
    };

    // Detect sidebar collapsed/expanded state and update button class
    function updateState() {
        var sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) {
            btn.classList.remove('sb-collapsed');
            btn.classList.add('sb-unknown');
            return;
        }
        var style = window.getComputedStyle(sidebar);
        var isCollapsed = sidebar.getAttribute('aria-hidden') === 'true' ||
                          style.display === 'none' ||
                          parseFloat(style.marginLeft) < 0 ||
                          sidebar.offsetWidth === 0;
        btn.classList.toggle('sb-collapsed', isCollapsed);
        btn.classList.remove('sb-unknown');
    }

    // Watch the sidebar element for DOM changes
    var sidebar = doc.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        var observer = new MutationObserver(function() { updateState(); });
        observer.observe(sidebar, {
            attributes: true,
            attributeFilter: ['class', 'style', 'aria-hidden'],
            childList: false,
            subtree: false,
        });
    }
    // Watch collapsedControl appearance/disappearance
    var cc = doc.querySelector('[data-testid="collapsedControl"]');
    if (cc) {
        var ccObserver = new MutationObserver(function() { updateState(); });
        ccObserver.observe(cc, {
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    }
    // Body-level fallback observer
    var bodyObserver = new MutationObserver(function(mutations) {
        for (var i = 0; i < mutations.length; i++) {
            var t = mutations[i];
            if (t.attributeName === 'class' || t.type === 'attributes') {
                updateState();
                break;
            }
        }
    });
    bodyObserver.observe(doc.body, {
        attributes: true,
        attributeFilter: ['class']
    });

    // Initial state
    updateState();

    // Refresh state after any click (catches Streamlit navigation)
    doc.addEventListener('click', function() {
        setTimeout(updateState, 300);
    });
''')


# ---- Import page modules ----
from pages.page_home import show as show_home
from pages.page_live_recommendation import show as show_live
from pages.page_model_comparison import show as show_comparison
from pages.page_sample_retrievals import show as show_retrievals
from pages.page_model_showdown import show as show_showdown
from pages.page_embedding_space import show as show_embedding
from pages.page_error_case import show as show_error
from pages.page_performance import show as show_performance
from pages.page_benchmark import show as show_benchmark
from pages.page_about import show as show_about

# ---- Page registry ----
PAGES = {
    "Home": {"icon": "🏠", "func": show_home},
    "Live Recommendation": {"icon": "🎯", "func": show_live},
    "Model Comparison": {"icon": "📊", "func": show_comparison},
    "Retrieval Gallery": {"icon": "🖼️", "func": show_retrievals},
    "Model Showdown": {"icon": "⚔️", "func": show_showdown},
    "Embedding Space": {"icon": "🔬", "func": show_embedding},
    "Error Analysis": {"icon": "❌", "func": show_error},
    "FAISS Benchmark": {"icon": "📐", "func": show_benchmark},
    "Performance": {"icon": "⚡", "func": show_performance},
    "About": {"icon": "👩‍💻", "func": show_about},
}

# ---- Premium Sidebar ----
with st.sidebar:
    # Brand header
    st.markdown(
        """
        <div style="padding: 1.2rem 1rem 1.5rem 1rem; text-align: center; 
                    background: linear-gradient(135deg, rgba(108,99,255,0.06), transparent);
                    border-radius: 14px; margin-bottom: 0.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🎯</div>
            <div style="font-weight: 800; font-size: 1.15rem; letter-spacing: -0.02em;
                        background: linear-gradient(135deg, #6C63FF, #8B83FF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;">
                Visual Product<br>Recommender
            </div>
            <div style="font-size: 0.7rem; opacity: 0.4; margin-top: 0.4rem; letter-spacing: 0.02em;">
                DEEP LEARNING · TENSORFLOW
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='margin: 0.25rem 0 0.75rem 0; opacity: 0.3;'>", unsafe_allow_html=True)

    # Current active page
    current_page = st.session_state.get("current_page", "Home")

    # Navigation buttons
    for page_name, page_info in PAGES.items():
        icon = page_info["icon"]
        is_active = page_name == current_page
        label = f"{icon}  {page_name}"

        if st.button(
            label,
            key=f"nav_{page_name.replace(' ', '_')}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state["current_page"] = page_name
            st.rerun()

    st.markdown("<hr style='margin: 0.75rem 0; opacity: 0.3;'>", unsafe_allow_html=True)

    # Theme toggle
    render_theme_toggle()

    # Side footer note
    st.markdown(
        """
        <div style="font-size: 0.65rem; text-align: center; opacity: 0.25; margin-top: 2rem; line-height: 1.5;">
            v1.0 &middot; Celebal Technologies
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---- Page routing ----
current_page = st.session_state.get("current_page", "Home")
page_func = PAGES.get(current_page, {}).get("func", show_home)
page_func()
