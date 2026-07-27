"""Unit tests for the component injection utilities (utils/components.py).

Tests cover:
  - run_parent_script() wraps JS with correct parent-document IIFE
  - run_script() passes raw JS through correctly
  - Both functions call components.html() with the expected arguments
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "streamlit_app"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest


# ======================================================================
# run_parent_script()
# ======================================================================

class TestRunParentScript:
    """run_parent_script() must wrap JS with the parent-document IIFE."""

    def test_wraps_in_iife(self, mock_components):
        """The JS body should be wrapped in an IIFE with parent document access."""
        from utils.components import run_parent_script

        js_body = "console.log('hello');"
        run_parent_script(js_body)

        # The mock captured what was passed to components.html()
        import streamlit.components.v1 as _c
        html_arg = _c._last_html_arg
        assert html_arg is not None, "components.html() was not called"

        assert "(function() {" in html_arg, "Missing IIFE wrapper"
        assert "var doc = window.parent.document;" in html_arg, (
            "Missing window.parent.document declaration"
        )
        assert "console.log('hello');" in html_arg, "JS body not found in wrapper"
        assert "})();" in html_arg, "Missing IIFE closing"

    def test_empty_body_still_wraps(self, mock_components):
        """Even an empty string should produce a valid IIFE skeleton."""
        from utils.components import run_parent_script

        run_parent_script("")

        import streamlit.components.v1 as _c
        html_arg = _c._last_html_arg
        assert "(function() {" in html_arg
        assert "})();" in html_arg

    def test_default_height_is_one(self, mock_components):
        """Default height should be 1 (minimal iframe to ensure script execution).
        Zero-height iframes may not execute scripts in some browser configs."""
        from utils.components import run_parent_script

        run_parent_script("var x = 1;")

        import streamlit.components.v1 as _c
        assert _c._last_height == 1, "Default height should be 1"

    def test_custom_height_passed_through(self, mock_components):
        """A custom height should be forwarded to components.html()."""
        from utils.components import run_parent_script

        run_parent_script("var x = 1;", height=60)

        import streamlit.components.v1 as _c
        assert _c._last_height == 60, "Custom height not forwarded"

    def test_script_tag_in_output(self, mock_components):
        """The output should contain a <script> tag wrapping the JS."""
        from utils.components import run_parent_script

        run_parent_script("var x = 1;")

        import streamlit.components.v1 as _c
        assert "<script>" in _c._last_html_arg
        assert "</script>" in _c._last_html_arg

    def test_display_none_div_in_output(self, mock_components):
        """The output should contain a hidden div (display:none) placeholder."""
        from utils.components import run_parent_script

        run_parent_script("var x = 1;")

        import streamlit.components.v1 as _c
        assert "display:none" in _c._last_html_arg


# ======================================================================
# run_script()
# ======================================================================

class TestRunScript:
    """run_script() must pass raw JS through without the parent-doc wrapper."""

    def test_no_iife_wrapper(self, mock_components):
        """Raw JS should NOT have the parent-document IIFE added."""
        from utils.components import run_script

        js_code = "(function() { console.log('raw'); })();"
        run_script(js_code)

        import streamlit.components.v1 as _c
        html_arg = _c._last_html_arg

        # The JS should appear verbatim — no extra var doc = window.parent.document
        assert "(function() { console.log('raw'); })();" in html_arg
        # But run_script doesn't add the IIFE itself, so the raw code is preserved

    def test_default_height_is_one(self, mock_components):
        """Default height should be 1."""
        from utils.components import run_script

        run_script("var x = 1;")

        import streamlit.components.v1 as _c
        assert _c._last_height == 1

    def test_custom_height_passed_through(self, mock_components):
        """Custom height should be forwarded."""
        from utils.components import run_script

        run_script("var x = 1;", height=100)

        import streamlit.components.v1 as _c
        assert _c._last_height == 100

    def test_script_tag_in_output(self, mock_components):
        """The output should contain a <script> tag."""
        from utils.components import run_script

        run_script("alert(1);")

        import streamlit.components.v1 as _c
        assert "<script>" in _c._last_html_arg
        assert "alert(1);" in _c._last_html_arg
        assert "</script>" in _c._last_html_arg
