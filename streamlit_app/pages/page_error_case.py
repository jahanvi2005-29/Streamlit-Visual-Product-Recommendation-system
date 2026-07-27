"""
Page 7 — Error Case Analysis
Concrete example where the baseline model failed and the Siamese succeeded.
Features an interactive before/after drag slider to compare results.
"""

import base64
import streamlit as st
from io import BytesIO
from PIL import Image
from utils.theme import get_theme
from utils.data_loader import get_image_path, load_error_case_example


def _img_to_data_uri(path, max_width=700):
    """Load an image and return a base64 data URI, resized to fit."""
    img = Image.open(path)
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def _comparison_slider_html(wrong_path, correct_path):
    """Generate the interactive before/after comparison slider HTML."""
    wrong_uri = _img_to_data_uri(wrong_path)
    correct_uri = _img_to_data_uri(correct_path)

    return f"""
    <div class="comparison-container">
        <div class="comparison-wrapper" id="cmp-wrapper">
            <!-- Baseline (wrong) — full width background -->
            <img src="{wrong_uri}" alt="Baseline — Incorrect retrieval" draggable="false">
            <!-- Siamese (correct) — overlaid with clip-path controlled by slider -->
            <div class="comparison-overlay" id="cmp-overlay">
                <img src="{correct_uri}" alt="Siamese — Correct retrieval" draggable="false">
            </div>
            <!-- Draggable handle -->
            <div class="comparison-handle" id="cmp-handle">
                <div class="comparison-handle-drag">
                    <span class="comparison-handle-drag-arrow">◀</span>
                    <span class="comparison-handle-drag-arrow">▶</span>
                </div>
            </div>
        </div>
        <div class="comparison-labels">
            <span class="comparison-label-left">Baseline — Incorrect</span>
            <span class="comparison-label-right">Siamese — Correct</span>
        </div>
    </div>

    <script>
    (function() {{
        var wrapper = document.getElementById('cmp-wrapper');
        var overlay = document.getElementById('cmp-overlay');
        var handle = document.getElementById('cmp-handle');
        if (!wrapper || !overlay || !handle) return;

        var isDragging = false;

        function updatePosition(e) {{
            var rect = wrapper.getBoundingClientRect();
            var clientX = e.touches ? e.touches[0].clientX : e.clientX;
            var x = ((clientX - rect.left) / rect.width) * 100;
            x = Math.max(2, Math.min(98, x));
            overlay.style.clipPath = 'inset(0 ' + (100 - x) + '% 0 0)';
            handle.style.left = x + '%';
        }}

        function onStart(e) {{
            isDragging = true;
            updatePosition(e);
        }}

        function onMove(e) {{
            if (!isDragging) return;
            e.preventDefault();
            updatePosition(e);
        }}

        function onEnd() {{
            isDragging = false;
        }}

        wrapper.addEventListener('mousedown', onStart);
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onEnd);

        wrapper.addEventListener('touchstart', onStart, {{passive: true}});
        document.addEventListener('touchmove', onMove, {{passive: false}});
        document.addEventListener('touchend', onEnd);
    }})();
    </script>
    """


def show():
    st.markdown(
        """
        <h1>❌ Error Case Analysis</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            A concrete failure case: the baseline model retrieves the wrong category, 
            while the Siamese Network gets it right. <strong>Drag the slider</strong> to 
            compare the two results side by side.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Load error case data ----
    error_df = load_error_case_example()
    error_info = None
    if error_df is not None and not error_df.empty:
        error_info = error_df.iloc[0]

    # ---- Interactive Comparison Slider ----
    wrong_path = get_image_path("error_case_baseline_wrong.png")
    correct_path = get_image_path("error_case_siamese_correct.png")

    if wrong_path and correct_path:
        html = _comparison_slider_html(wrong_path, correct_path)
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Error case images not found.")

    # ---- Callout boxes below the slider ----
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="comparison-callout">
                <span style="font-size:1.2rem;">❌</span>
                <span><strong>Baseline</strong> retrieved a <strong>T-shirt</strong> — 
                wrong category. Generic ImageNet features can't distinguish fine-grained 
                fashion differences.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="comparison-callout comparison-callout-success">
                <span style="font-size:1.2rem;">✅</span>
                <span><strong>Siamese Network</strong> retrieved a <strong>Shirt</strong> — 
                correct! Triplet-loss training learned a specialized fashion embedding space.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Why this happens ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Why Does This Happen?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="custom-card">
                <h4>🏗️ Baseline Limitation</h4>
                <p style="font-size: 0.9rem; opacity: 0.85;">
                    ResNet50 pretrained on ImageNet was trained to classify 1,000 general 
                    object categories (dogs, cars, food, etc.). Its feature representations 
                    are optimized for <strong>generic visual recognition</strong>, not for 
                    fine-grained fashion attributes. Two different clothing items (shirt vs.
                    T-shirt) may appear similar in parts of this generic feature space.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="custom-card" style="border-color: #6C63FF; 
                        background: rgba(108,99,255,0.05);">
                <h4>🏆 Siamese Advantage</h4>
                <p style="font-size: 0.9rem; opacity: 0.85;">
                    The Siamese Network was trained with <strong>triplet loss</strong>, 
                    which explicitly pulls anchor and positive (same-category) images closer 
                    while pushing anchor and negative (different-category) images apart. 
                    This creates a <strong>specialized fashion embedding space</strong> where 
                    subtle differences between shirt types are preserved and amplified.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Error case details from CSV ----
    t = get_theme()
    if error_info is not None:
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Error Case Details (from evaluation)")

        st.markdown(
            f"""
            <table style="width:100%; border-collapse: collapse; border-radius: 12px; overflow: hidden;">
                <thead>
                    <tr style="background: rgba(108,99,255,0.1);">
                        <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Field</th>
                        <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Query Category</td>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">
                            <span class="badge badge-accent">{error_info.get('Query_Category', 'N/A')}</span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Baseline Retrieved</td>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">
                            <span class="badge badge-error">{error_info.get('Baseline_Retrieved', 'N/A')} ✗</span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Baseline Correct?</td>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">
                            <span class="badge badge-error">{str(error_info.get('Baseline_Correct', 'N/A'))}</span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Siamese Retrieved</td>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">
                            <span class="badge badge-success">{error_info.get('Siamese_Retrieved', 'N/A')} ✓</span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Siamese Correct?</td>
                        <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">
                            <span class="badge badge-success">{str(error_info.get('Siamese_Correct', 'N/A'))}</span>
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )
