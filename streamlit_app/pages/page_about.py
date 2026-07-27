"""
Page 9 — About / Author
Project summary, author info, and how-it-works visual explainer.
"""

import streamlit as st


def show():
    # ---- Author Header ----
    st.markdown(
        """
        <div class="hero-section">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">👩‍💻</div>
            <h1 class="hero-title">About the Project</h1>
            <p class="hero-subtitle">
                Visual Product Recommendation System — a deep learning project 
                exploring metric learning for fashion image retrieval.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Author Info ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 5rem; margin-bottom: 0.5rem;">👩‍💻</div>
                <h3>Jahanvi Gupta</h3>
                <p style="opacity: 0.7; font-size: 0.9rem;">
                    Data Science Intern<br>
                    @ Celebal Technologies
                </p>
                <div style="margin-top: 1rem;">
                    <span class="tech-badge">Python</span>
                    <span class="tech-badge">TensorFlow</span>
                    <span class="tech-badge">Deep Learning</span>
                    <span class="tech-badge">Computer Vision</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <h2>Project Summary</h2>
            <p style="font-size: 1rem; line-height: 1.7; opacity: 0.85;">
                This project implements and compares three approaches to content-based 
                visual product recommendation using a subset of the <strong>Fashion Product 
                Images Dataset</strong> from Kaggle (1,199 images across 4 categories).
            </p>
            <p style="font-size: 1rem; line-height: 1.7; opacity: 0.85;">
                The core idea: <strong>find visually similar products using only their images</strong>
                — no text, no tags, no metadata. Each image is encoded into a 128-dimensional
                embedding vector, and cosine similarity between embeddings determines visual
                similarity.
            </p>
            <p style="font-size: 1rem; line-height: 1.7; opacity: 0.85;">
                The <strong>Siamese Network with triplet loss</strong> achieves the best performance
                (99.7% Precision@5) by learning a specialized embedding space where visually
                similar items naturally cluster together.
            </p>
            """,
            unsafe_allow_html=True,
        )

    # ---- How It Works ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## How It Works — Step by Step")

    steps = [
        ("1", "🖼️", "Input Image", "Upload or select a fashion product image"),
        ("2", "🧠", "CNN Encoder", "Pass through ResNet50 backbone to extract features"),
        ("3", "📐", "Embedding", "Project features into a 128-dimensional embedding space"),
        ("4", "📏", "Similarity Search", "Cosine similarity against all catalog embeddings"),
        ("5", "🎯", "Top-K Results", "Return the most visually similar products"),
    ]

    for i, (step_num, icon, title, desc) in enumerate(steps):
        cols = st.columns([1, 5])
        with cols[0]:
            st.markdown(
                f"""
                <div style="width: 48px; height: 48px; border-radius: 50%; 
                            background: rgba(108,99,255,0.15); display: flex; align-items: center; 
                            justify-content: center; font-size: 1.2rem; font-weight: 700;
                            color: #6C63FF; margin: 0 auto;">
                    {icon}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f"""
                <div style="padding: 0.5rem 0;">
                    <strong style="font-size: 1.1rem;">{title}</strong>
                    <br>
                    <span style="opacity: 0.7; font-size: 0.9rem;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if i < len(steps) - 1:
            st.markdown(
                """
                <div style="text-align: center; opacity: 0.3; font-size: 1.2rem; 
                            padding: 0.25rem 0;">↓</div>
                """,
                unsafe_allow_html=True,
            )

    # ---- Tech Stack Details ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Technology Stack")

    tech_data = [
        ("Python 3.12", "Core programming language"),
        ("TensorFlow/Keras 2.x", "Deep learning framework — model training & inference"),
        ("ResNet50", "CNN backbone for feature extraction (pretrained on ImageNet)"),
        ("scikit-learn", "t-SNE visualization, evaluation metrics"),
        ("NumPy", "Numerical computing, embedding storage, similarity computation"),
        ("pandas", "Data loading, manifest management"),
        ("Streamlit", "Web application framework for the interactive dashboard"),
        ("Plotly", "Interactive data visualizations & charts"),
        ("Pillow", "Image preprocessing & display"),
    ]

    for tech, description in tech_data:
        st.markdown(
            f"""
            <div class="custom-card" style="padding: 0.75rem 1.2rem; margin-bottom: 0.3rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{tech}</strong>
                    <span style="opacity: 0.6; font-size: 0.85rem;">{description}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Dataset note ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("## Dataset")

    st.markdown(
        """
        <div class="custom-card">
            <p style="font-size: 0.95rem; line-height: 1.6; opacity: 0.85;">
                <strong>Fashion Product Images Dataset</strong> (Kaggle)<br>
                A subset of <strong>1,199 images</strong> across <strong>4 categories</strong>:
                Shirts (299), Dresses (300), T-shirts (300), and Watches (300).<br><br>
                The original evaluation also included a <strong>Shoes</strong> category — 
                sample retrieval results for Shoes can be seen in the Retrieval Gallery page, 
                demonstrating the model's ability to generalize across product types beyond 
                the 4 categories selected for the final benchmark.<br><br>
                Each image is 60×80 pixels (RGB). Images are resized to 224×224 for 
                model input. The dataset is balanced across categories to prevent 
                biased similarity comparisons.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Final note ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0;">
            <p style="opacity: 0.4; font-size: 0.75rem;">
                Visual Product Recommendation System · Deep Learning · Computer Vision · Metric Learning
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
