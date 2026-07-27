"""Shared pytest fixtures and mocks for the test suite."""

import pytest


class SessionStateMock(dict):
    """A dict subclass that also supports attribute access.

    Streamlit's st.session_state supports both:
      st.session_state["key"] = value   (dict-style)
      st.session_state.key = value      (attribute-style)

    This mock supports both by routing __setattr__/__getattr__ to the
    underlying dict storage.
    """

    def __getattr__(self, key):
        if key.startswith("_"):
            raise AttributeError(key)
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch):
    """Mock streamlit.session_state and other Streamlit internals.

    Without this fixture, importing utils.theme would try to access
    st.session_state before any Streamlit runtime exists, causing errors.
    """
    import streamlit as st

    mock_state = SessionStateMock({"dark_mode": True})

    monkeypatch.setattr(st, "session_state", mock_state)

    # st.button: no-op that returns False (not clicked)
    monkeypatch.setattr(st, "button", lambda *a, **kw: False)

    # st.rerun: no-op
    monkeypatch.setattr(st, "rerun", lambda: None)

    # st.markdown: return the string (for testing HTML output)
    monkeypatch.setattr(st, "markdown", lambda text, **kw: text)

    return mock_state


@pytest.fixture
def mock_components(monkeypatch):
    """Mock streamlit.components.v1.html to capture last arguments.

    Used by test_components.py to verify what was passed to components.html().
    """
    import streamlit.components.v1 as _components

    _components._last_html_arg = None
    _components._last_height = None

    def _mock_html(html, height=0, **kwargs):
        _components._last_html_arg = html
        _components._last_height = height
        return None

    monkeypatch.setattr(_components, "html", _mock_html)
    return _components
