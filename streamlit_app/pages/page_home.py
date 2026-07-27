"""
Page 1 — Home / Overview
Hero section, metric cards, architecture flow diagram, tech stack badges.
"""

import streamlit as st
from utils.theme import get_theme


def show():
    theme = get_theme()

    # ---- Hero Section ----
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">Visual Product Recommendation System</h1>
            <p class="hero-subtitle">
                Finding visually similar fashion products using deep learning — no text,
                no tags, no metadata. Just pure visual similarity.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Problem Statement ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("## The Problem")
        st.markdown(
            """
            Traditional product recommendation systems rely heavily on text metadata — 
            product titles, descriptions, and manually assigned tags. This approach fails when:
            
            - **Text data is incomplete or missing** from the catalog
            - **Products look similar but have different descriptions** (e.g., "sneakers" vs "athletic shoes")
            - **Visual attributes matter more than text** (pattern, color, shape)
            - **New products arrive** without proper tagging
            
            **Our solution:** A purely visual approach that compares products by their appearance
            alone, using deep convolutional neural networks to generate image embeddings and
            cosine similarity to find the closest matches — exactly like a visual search engine.
            """
        )

    with col2:
        st.markdown("## The Approach")
        st.markdown(
            """
            We benchmarked **three progressively stronger approaches** on the same dataset:
            
            1. **Baseline** — Pretrained ResNet50 (ImageNet), no fine-tuning
            2. **Transfer Learning** — ResNet50 fine-tuned on product categories
            3. **Siamese Network** — Custom 128-dim embedding trained with triplet loss
            
            **Winner:** The Siamese Network achieves **99.7% Precision@5** by learning
            a specialized embedding space where visually similar products naturally cluster
            together.
            """
        )

    # ---- Metric Cards ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Project at a Glance")

    cols = st.columns(4)
    metrics = [
        ("1,199", "Catalog Images"),
        ("3", "Models Benchmarked"),
        ("4", "Product Categories"),
        ("128-dim", "Embedding Size"),
    ]
    for i, (value, label) in enumerate(metrics):
        with cols[i]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---- Architecture Flow Diagram ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Architecture Flow")

    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; 
                    flex-wrap: wrap; gap: 0.75rem; padding: 1.5rem 0;">
            <div class="flow-box">
                🖼️<br>Query Image<br>
                <span style="font-size:0.7rem;opacity:0.6;">224×224</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">
                🧠<br>CNN Backbone<br>
                <span style="font-size:0.7rem;opacity:0.6;">ResNet50</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">
                📐<br>Embedding Vector<br>
                <span style="font-size:0.7rem;opacity:0.6;">128-dim</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-box">
                📏<br>Cosine Similarity<br>
                <span style="font-size:0.7rem;opacity:0.6;">vs Catalog</span>
            </div>
            <span class="flow-arrow">→</span>
            <div class="flow-box" style="border-color: #6C63FF; background: rgba(108,99,255,0.08);">
                🎯<br>Top-K Results<br>
                <span style="font-size:0.7rem;opacity:0.6;">Most Similar</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Tech Stack ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Tech Stack")

    techs = [
        "Python", "TensorFlow/Keras", "scikit-learn", "pandas",
        "NumPy", "Streamlit", "Plotly", "Pillow"
    ]
    cols = st.columns(len(techs))
    for i, tech in enumerate(techs):
        with cols[i]:
            st.markdown(f'<div class="tech-badge">{tech}</div>', unsafe_allow_html=True)

    # ---- Quick Stats Table ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Final Benchmark Results")

    t = theme
    st.markdown(
        f"""
        <table style="width:100%; border-collapse: collapse; border-radius: 12px; overflow: hidden;">
            <thead>
                <tr style="background: rgba(108,99,255,0.1);">
                    <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Model</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Precision@5</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Recall@5</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Baseline</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.972</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.0163</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">Transfer Learning</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.990</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">0.0166</td>
                </tr>
                <tr style="background: rgba(108,99,255,0.05);">
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; font-weight: 600;">🏆 Siamese Network</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; color: #6C63FF; font-weight: 700;">0.997</td>
                    <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; color: #6C63FF; font-weight: 700;">0.0167</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="text-align: center; font-size: 0.8rem; opacity: 0.6; margin-top: 0.5rem;">
            Dataset: 1,199 fashion images across 4 categories • Metric: Cosine Similarity
        </p>
        """,
        unsafe_allow_html=True,
    )
