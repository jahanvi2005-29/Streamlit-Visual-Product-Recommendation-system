"""Unit tests for the theme management module (utils/theme.py).

Tests cover:
  - init_theme() session-state initialization
  - get_theme() colour dictionary correctness in dark / light mode
  - get_css() output contains expected CSS selectors and colour values
"""

import sys
from pathlib import Path

# Ensure the project root (one level above tests/) is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "streamlit_app"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest


# ======================================================================
# init_theme()
# ======================================================================

class TestInitTheme:
    """init_theme() should set dark_mode=True when not already present."""

    def test_sets_default_when_missing(self, mock_streamlit):
        """If dark_mode is absent from session_state, init_theme sets it to True."""
        import streamlit as st
        st.session_state.pop("dark_mode", None)  # ensure absent

        from utils.theme import init_theme
        init_theme()

        assert st.session_state.dark_mode is True

    def test_does_not_override_existing(self, mock_streamlit):
        """If dark_mode is already present, init_theme leaves it untouched."""
        import streamlit as st
        st.session_state.dark_mode = False  # light mode

        from utils.theme import init_theme
        init_theme()

        assert st.session_state.dark_mode is False


# ======================================================================
# get_theme()
# ======================================================================

class TestGetTheme:
    """get_theme() should return correct color dictionaries."""

    def test_dark_mode_colors(self, mock_streamlit):
        """Dark mode returns DARK_BG and dark-mode-specific accent keys."""
        import streamlit as st
        st.session_state.dark_mode = True

        from utils.theme import get_theme
        t = get_theme()

        assert t["is_dark"] is True
        assert t["mode"] == "dark"
        assert t["bg"] == "#090D16"
        assert t["text"] == "#F1F5F9"
        assert t["text_secondary"] == "#94A3B8"
        assert t["accent"] == "#6366F1"

    def test_light_mode_colors(self, mock_streamlit):
        """Light mode returns LIGHT_BG and light-mode-specific values."""
        import streamlit as st
        st.session_state.dark_mode = False

        from utils.theme import get_theme
        t = get_theme()

        assert t["is_dark"] is False
        assert t["mode"] == "light"
        assert t["bg"] == "#F8FAFC"
        assert t["text"] == "#0F172A"
        assert t["text_secondary"] == "#64748B"
        assert t["accent"] == "#6366F1"  # accent is theme-independent

    def test_defaults_to_dark(self, mock_streamlit):
        """If session_state has no dark_mode key, get_theme defaults to dark."""
        import streamlit as st
        st.session_state.pop("dark_mode", None)

        from utils.theme import get_theme
        t = get_theme()

        assert t["is_dark"] is True
        assert t["mode"] == "dark"

    def test_all_expected_keys_present(self, mock_streamlit):
        """Both themes return the full set of keys required by pages."""
        import streamlit as st

        from utils.theme import get_theme
        expected_keys = {
            "is_dark", "bg", "card", "card_hover", "text",
            "text_secondary", "border", "accent", "accent_light",
            "accent_dark", "mode",
        }

        for dark in (True, False):
            st.session_state.dark_mode = dark
            t = get_theme()
            assert set(t.keys()) == expected_keys, f"Missing keys in {'dark' if dark else 'light'} mode"


# ======================================================================
# get_css()
# ======================================================================

SHARED_SELECTORS = [
    "collapsedControl",        # sidebar reopen arrow
    "#MainMenu",               # Streamlit chrome hide
    "fadeInUp",                # entrance animation
    "metric-card",             # premium card style
    "custom-card",
    "flow-box",
    "section-divider",
    "sim-bar",
    "badge",
    "tech-badge",
    "comparison-container",    # before/after slider styles
    "compare-row",             # side-by-side compare
]

DARK_ONLY_MARKERS = ["#090D16", "rgba(15, 23, 42, 0.65)"]
LIGHT_ONLY_MARKERS = ["#F8FAFC", "rgba(255, 255, 255, 0.85)"]


class TestGetCss:
    """get_css() should produce correct CSS for each theme."""

    def test_dark_css_contains_dark_bg(self, mock_streamlit):
        """Dark-mode CSS includes the dark background colour."""
        import streamlit as st
        st.session_state.dark_mode = True

        from utils.theme import get_css
        css = get_css()

        assert "#090D16" in css

    def test_light_css_contains_light_bg(self, mock_streamlit):
        """Light-mode CSS includes the light background colour."""
        import streamlit as st
        st.session_state.dark_mode = False

        from utils.theme import get_css
        css = get_css()

        assert "#F8FAFC" in css

    @pytest.mark.parametrize("selector", SHARED_SELECTORS)
    def test_shared_selectors_present_dark(self, mock_streamlit, selector):
        """All critical CSS selectors appear in dark-mode CSS."""
        import streamlit as st
        st.session_state.dark_mode = True

        from utils.theme import get_css
        css = get_css()

        assert selector in css, f"Missing selector: {selector}"

    @pytest.mark.parametrize("selector", SHARED_SELECTORS)
    def test_shared_selectors_present_light(self, mock_streamlit, selector):
        """All critical CSS selectors appear in light-mode CSS."""
        import streamlit as st
        st.session_state.dark_mode = False

        from utils.theme import get_css
        css = get_css()

        assert selector in css, f"Missing selector: {selector}"

    @pytest.mark.parametrize("marker", DARK_ONLY_MARKERS)
    def test_dark_markers_not_in_light(self, mock_streamlit, marker):
        """Dark-mode-specific colour values should NOT appear in light CSS."""
        import streamlit as st
        st.session_state.dark_mode = False

        from utils.theme import get_css
        css = get_css()

        assert marker not in css, f"Dark colour leaked into light CSS: {marker}"

    @pytest.mark.parametrize("marker", LIGHT_ONLY_MARKERS)
    def test_light_markers_not_in_dark(self, mock_streamlit, marker):
        """Light-mode-specific colour values should NOT appear in dark CSS."""
        import streamlit as st
        st.session_state.dark_mode = True

        from utils.theme import get_css
        css = get_css()

        assert marker not in css, f"Light colour leaked into dark CSS: {marker}"


# ======================================================================
# render_theme_toggle()
# ======================================================================

class TestRenderThemeToggle:
    """render_theme_toggle() toggles dark_mode when button is clicked."""

    def test_toggle_dark_to_light(self, mock_streamlit, monkeypatch):
        """Clicking the toggle in dark mode switches to light."""
        import streamlit as st
        from utils.theme import render_theme_toggle

        st.session_state.dark_mode = True
        # Make st.button return True (simulating a click)
        monkeypatch.setattr(st, "button", lambda *a, **kw: True)

        render_theme_toggle()

        assert st.session_state.dark_mode is False

    def test_toggle_light_to_dark(self, mock_streamlit, monkeypatch):
        """Clicking the toggle in light mode switches to dark."""
        import streamlit as st
        from utils.theme import render_theme_toggle

        st.session_state.dark_mode = False
        monkeypatch.setattr(st, "button", lambda *a, **kw: True)

        render_theme_toggle()

        assert st.session_state.dark_mode is True

    def test_no_toggle_when_not_clicked(self, mock_streamlit):
        """When the toggle button is NOT clicked, dark_mode should be unchanged."""
        import streamlit as st
        from utils.theme import render_theme_toggle

        st.session_state.dark_mode = True
        # Default mock returns False (not clicked)

        render_theme_toggle()

        assert st.session_state.dark_mode is True

    def test_header_visible_in_dark(self, mock_streamlit):
        """The header (containing collapsedControl) must have visibility:visible in dark mode."""
        import streamlit as st
        st.session_state.dark_mode = True

        from utils.theme import get_css
        css = get_css()

        assert "header {visibility: visible !important;" in css

    def test_header_visible_in_light(self, mock_streamlit):
        """The header (containing collapsedControl) must have visibility:visible in light mode."""
        import streamlit as st
        st.session_state.dark_mode = False

        from utils.theme import get_css
        css = get_css()

        assert "header {visibility: visible !important;" in css

    def test_collapsed_control_is_hidden(self, mock_streamlit):
        """The collapsedControl must now have display:none (hidden — ☰ hamburger is the sole toggle)."""
        import streamlit as st

        from utils.theme import get_css
        for dark in (True, False):
            st.session_state.dark_mode = dark
            css = get_css()
            assert "display: none !important" in css, f"Missing display:none on collapsedControl in {'dark' if dark else 'light'} mode"
            assert "collapsedControl" in css
