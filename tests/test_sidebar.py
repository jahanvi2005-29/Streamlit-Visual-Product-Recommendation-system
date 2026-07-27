"""Tests for the sidebar toggle button rendered in app.py.

The sidebar button now uses a two-part approach:
  1. st.markdown(unsafe_allow_html=True)      — renders button HTML + CSS
  2. run_parent_script(...)                   — executes JS (onclick, MutationObserver)
     (which internally calls components.v1.html)
  Because Streamlit 1.60.0 strips inline event handlers from st.markdown.

These tests parse the raw source strings to verify both parts are correct.
"""

import sys
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "streamlit_app"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _extract_markdown_block(filepath, marker_id="sbt-btn"):
    """Read app.py and find the st.markdown block containing the given id."""
    src = filepath.read_text(encoding="utf-8")

    # Find the st.markdown call — look for the button id
    start = src.find(marker_id)
    if start == -1:
        pytest.fail(f"Could not find '{marker_id}' in app.py")

    # Walk backward to find the opening triple-quote of the markdown call
    qstart = src.rfind('"""', 0, start)
    if qstart == -1:
        pytest.fail("Could not locate opening triple-quote for sidebar markdown")

    # Walk forward to find the closing triple-quote
    qend = src.find('"""', qstart + 3)
    if qend == -1:
        pytest.fail("Could not locate closing triple-quote for sidebar markdown")

    return src[qstart + 3: qend]


def _extract_js_block(filepath, marker="getElementById('sbt-btn')"):
    """Read app.py and find the run_parent_script() JS block containing the given marker.

    The JS is passed as a triple-quoted string argument to run_parent_script().
    This function finds that marker within the Python source, walks backward
    to the opening triple-quote of that function call, then extracts the full
    JS string.
    """
    src = filepath.read_text(encoding="utf-8")

    start = src.find(marker)
    if start == -1:
        pytest.fail(f"Could not find '{marker}' JS block in app.py")

    # Walk backward to find the opening triple-quote of run_parent_script()
    qstart = src.rfind("'''", 0, start)
    if qstart == -1:
        pytest.fail("Could not locate opening triple-quote for run_parent_script JS")

    # Walk forward to find the closing triple-quote
    qend = src.find("'''", qstart + 3)
    if qend == -1:
        pytest.fail("Could not locate closing triple-quote for run_parent_script JS")

    return src[qstart + 3: qend]


APP_PY = PROJECT_ROOT / "streamlit_app" / "app.py"
SIDEBAR_HTML = _extract_markdown_block(APP_PY)
COMPONENTS_JS = _extract_js_block(APP_PY)


class TestSidebarButtonMarkup:
    """Verify the sidebar toggle button HTML (+CSS) in st.markdown."""

    def test_button_element_present(self):
        """The button with id 'sbt-btn' must exist in the markdown HTML."""
        assert 'id="sbt-btn"' in SIDEBAR_HTML, "Button element not found"

    def test_no_display_none(self):
        """The button must NOT have display:none (previous bug)."""
        assert "display: none" not in SIDEBAR_HTML, (
            "display:none found in sidebar button HTML — the button would be invisible!"
        )

    def test_style_uses_position_fixed(self):
        """Button must use position fixed for top-left placement."""
        assert "position: fixed" in SIDEBAR_HTML or "position:fixed" in SIDEBAR_HTML

    def test_style_has_frosted_glass(self):
        """Button should have frosted glass styling (backdrop-filter)."""
        assert "backdrop-filter" in SIDEBAR_HTML

    def test_button_has_aria_label(self):
        """Button should have an aria-label or title for accessibility."""
        has_aria = 'aria-label="Toggle sidebar"' in SIDEBAR_HTML
        has_title = 'title="Toggle sidebar"' in SIDEBAR_HTML
        assert has_aria or has_title, "Missing aria-label or title"

    def test_hover_style_present(self):
        """There should be a :hover style for the button."""
        assert "#sbt-btn:hover" in SIDEBAR_HTML or "#sbt-btn:hover" in SIDEBAR_HTML

    def test_no_inline_onclick_in_markdown(self):
        """The markdown should NOT contain an inline onclick (it's in components.html)."""
        assert "onclick=" not in SIDEBAR_HTML, (
            "Inline onclick found in st.markdown — it would be stripped by Streamlit 1.60.0 sanitizer. "
            "Move JS logic to components.v1.html instead."
        )

    def test_no_script_tag_in_markdown(self):
        """The markdown should NOT contain a <script> tag (it's in components.html)."""
        assert "<script>" not in SIDEBAR_HTML, (
            "<script> tag found in st.markdown — it would be stripped by Streamlit 1.60.0 sanitizer. "
            "Move JS logic to components.v1.html instead."
        )


class TestComponentsJS:
    """Verify the JavaScript logic in components.v1.html is correct."""

    def test_onclick_references_collapsed_control(self):
        """The onclick handler must query collapsedControl."""
        assert "collapsedControl" in COMPONENTS_JS, (
            "onclick handler does not reference collapsedControl"
        )

    def test_uses_doc_for_parent_access(self):
        """The script must reference `doc` (pre-declared by run_parent_script as
        window.parent.document) to access the main page from the iframe."""
        # doc is declared by the run_parent_script() wrapper as:
        #   var doc = window.parent.document;
        # The JS body should reference doc (not window.parent.document directly,
        # since that's abstracted by the utility).
        assert "doc." in COMPONENTS_JS, (
            "Missing `doc.` reference — the script should use `doc` to access "
            "the parent document (declared by run_parent_script's IIFE wrapper)."
        )

    def test_onclick_dispatches_click_event(self):
        """The onclick should dispatch a MouseEvent on the collapsedControl.

        Previously used .click(), now uses dispatchEvent(new MouseEvent('click', ...))
        which is more robust for hidden (display:none) elements because it
        dispatches a synthetic event that bubbles up to React's event delegation.
        """
        has_dispatch = "dispatchEvent" in COMPONENTS_JS
        has_mouse_event = "MouseEvent" in COMPONENTS_JS
        assert has_dispatch and has_mouse_event, (
            "onclick should dispatch a MouseEvent on collapsedControl. "
            f"dispatchEvent={'✓' if has_dispatch else '✗'}, "
            f"MouseEvent={'✓' if has_mouse_event else '✗'}"
        )

    def test_mutation_observer_present(self):
        """The components JS should include a MutationObserver call."""
        assert "MutationObserver" in COMPONENTS_JS

    def test_observes_sidebar(self):
        """The observer should watch the stSidebar element."""
        assert "stSidebar" in COMPONENTS_JS

    def test_detects_aria_hidden(self):
        """State detection should check aria-hidden."""
        assert "aria-hidden" in COMPONENTS_JS

    def test_detects_display_none(self):
        """State detection should check style.display."""
        assert ".display" in COMPONENTS_JS

    def test_observer_attribute_filter_valid(self):
        """attributeFilter should only contain valid exact attribute names."""
        match = re.search(
            r'attributeFilter\s*:\s*\[(.*?)\]',
            COMPONENTS_JS,
            re.DOTALL,
        )
        if not match:
            pytest.fail("Could not find attributeFilter array in MutationObserver")
        filters = re.findall(r"'([^']+)'", match.group(1))
        valid_attrs = {"class", "style", "aria-hidden"}
        for attr in filters:
            assert attr in valid_attrs, (
                f"Invalid attributeFilter entry: '{attr}'. "
                f"Only exact attribute names allowed (e.g. class, style, aria-hidden)"
            )

    def test_has_fallback_logic(self):
        """The JS should include a fallback for when collapsedControl is not found."""
        assert "fallback" in COMPONENTS_JS.lower() or "stSidebar" in COMPONENTS_JS, (
            "Missing fallback logic for when collapsedControl is unavailable"
        )

    def test_first_line_finds_button(self):
        """The script should get the button from parent document first."""
        assert "doc.getElementById('sbt-btn')" in COMPONENTS_JS or 'doc.getElementById("sbt-btn")' in COMPONENTS_JS, (
            "Script must find the button via parent document reference"
        )
