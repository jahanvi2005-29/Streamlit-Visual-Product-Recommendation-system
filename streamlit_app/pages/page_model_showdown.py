"""
Page 5 — Model Showdown
Head-to-head comparison: same query, top-1 result from all 3 models.
"""

import streamlit as st
from utils.theme import get_theme
from utils.data_loader import get_image_path


def show():
    st.markdown(
        """
        <h1>⚔️ Model Showdown</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Same query image. Same catalog. Three different models. See who returns 
            the best top-1 result.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Full-width showdown image ----
    img_path = get_image_path("side_by_side_top1_comparison.png")
    if img_path:
        st.image(img_path, use_container_width=True)
    else:
        st.info("Showdown image not found.")

    # ---- Analysis ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center;">
                <h3>🏗️ Baseline</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    Generic ImageNet features. Often retrieves the correct category but 
                    can mismatch visual style. No fine-tuning means the features are 
                    optimized for natural images, not fashion products.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center;">
                <h3>🔧 Transfer Learning</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    Fine-tuned on fashion categories. Better category alignment than baseline,
                    but still limited by training on only 4 coarse labels — it learns
                    "what a shirt looks like" but not fine-grained style differences.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center; border-color: #6C63FF; 
                        background: rgba(108,99,255,0.05);">
                <h3>🏆 Siamese Network</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    Trained with triplet loss for metric learning. The embedding space
                    is explicitly optimized so that visually similar items are close together.
                    This produces the most visually consistent and category-accurate results.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Summary table ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Head-to-Head Summary")

    t = get_theme()

    st.markdown(
        f"""
        <table style="width:100%; border-collapse: collapse; border-radius: 12px; overflow: hidden;">
            <thead>
                <tr style="background: rgba(108,99,255,0.1);">
                    <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Metric</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Baseline</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Transfer Learning</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600; color: #6C63FF;">Siamese</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Precision@5</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.972</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.990</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; font-weight: 700; color: #10B981;">0.997 ✅</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Recall@5</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.0163</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.0166</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; font-weight: 700; color: #10B981;">0.0167 ✅</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Training Data</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">None (frozen)</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">1199 labels</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">Triplet sampling</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Method</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">ResNet50 (frozen)</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">Fine-tuned ResNet50</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; font-weight: 600; color: #6C63FF;">Triplet Loss Network</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); 
                    border-radius: 12px; padding: 1.5rem;">
            <h3>💡 Takeaway</h3>
            <p style="opacity: 0.85;">
                The Siamese Network outperforms both alternatives because it was explicitly 
                trained to <strong>pull visually similar items together</strong> and 
                <strong>push dissimilar items apart</strong> in embedding space — a task 
                that neither generic ImageNet features nor coarse category labels can achieve.
                The result is a specialized embedding that captures fine-grained visual 
                attributes like shape, pattern, color, and style.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
