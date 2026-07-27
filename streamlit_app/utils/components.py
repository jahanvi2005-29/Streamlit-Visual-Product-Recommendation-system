"""
Reusable utilities for injecting interactive UI components.

Streamlit 1.60.0+ strips inline event handlers and <script> tags from
st.markdown(unsafe_allow_html=True). To work around this, we use a two-part
pattern:

  1. **st.markdown()** renders HTML + CSS in the *parent document*
     (where ``position: fixed`` works correctly for overlays).
  2. **st.components.v1.html()** executes JavaScript in a *real iframe*
     context where the browser runs scripts as expected.

The functions in this module handle the ``components.v1.html()`` part,
providing clean, reusable wrappers so you never need to call
``components.html()`` directly for this pattern.

Usage example::

    from utils.components import run_parent_script

    # Part 1 — HTML + CSS in parent document
    st.markdown('<button id="my-btn">Click me</button><style>...</style>',
                unsafe_allow_html=True)

    # Part 2 — JS via components iframe (auto-wraps with parent doc access)
    run_parent_script('''
        var btn = doc.getElementById('my-btn');
        if (!btn) return;
        btn.onclick = function() { alert('Hello!'); };
    ''')
"""

import streamlit.components.v1 as _components


def run_script(js_code: str, height: int = 1):
    """Execute raw JavaScript in a real iframe context.

    Streamlit's ``st.markdown`` sanitizer strips inline event handlers
    and ``<script>`` tags. This function wraps JS inside
    ``st.components.v1.html()`` which runs inside a real iframe where
    JavaScript executes correctly.

    The script runs as-is inside a ``<script>`` tag. For accessing the
    parent (main) page DOM, use ``window.parent.document`` directly, or
    use :func:`run_parent_script` which handles this automatically.

    Args:
        js_code:
            Complete JavaScript source code (e.g. an IIFE or standalone
            script). The code is placed verbatim inside a ``<script>``
            tag, so include any wrapping IIFE if needed.
        height:
            Height of the iframe in px. Default ``1`` (minimal; zero-height
            iframes may not execute scripts in some browser configurations).
    """
    _components.html(
        f"<div style=\"display:none;\"></div><script>{js_code}</script>",
        height=height,
    )


def run_parent_script(js_body: str, height: int = 1):
    """Execute JavaScript in the context of the **parent** (main) page DOM.

    This is the standard helper for components that were rendered via
    ``st.markdown()`` and need JavaScript interactivity. It wraps
    *js_body* in an IIFE that accesses the parent document, so you
    don't need to deal with ``window.parent.document`` manually.

    Inside *js_body* you can reference:

    * ``doc`` — the parent ``document`` object
    * All standard browser APIs (``window``, ``Element``, etc.)

    Example::

        run_parent_script('''
            var btn = doc.getElementById('my-button');
            if (!btn) return;
            btn.onclick = function() { console.log('clicked'); };
        ''')

    The IIFE wrapper and ``doc`` declaration are added automatically.
    If your code defines functions or needs a different setup, use
    :func:`run_script` instead and handle ``window.parent.document``
    yourself.

    Args:
        js_body:
            JavaScript code body. **Do not** include the IIFE wrapper
            or ``var doc = window.parent.document;`` — those are added
            automatically. The body runs after ``doc`` is available.
        height:
            Height of the hidden iframe in px. Default ``1`` (minimal — zero-height
            iframes may not execute scripts in some browser configurations).
    """
    wrapped = (
        "(function() {\n"
        "var doc = window.parent.document;\n"
        f"{js_body}\n"
        "})();"
    )
    _components.html(
        f"<div style=\"display:none;\"></div><script>{wrapped}</script>",
        height=height,
    )
