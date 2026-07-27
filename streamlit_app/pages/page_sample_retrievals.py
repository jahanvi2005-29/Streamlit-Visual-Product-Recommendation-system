"""
Page 4 — Sample Retrievals Gallery
Per-model tabs showing retrieval grids and category-specific sample retrievals.
"""

import streamlit as st
from utils.data_loader import get_image_path


def show():
    st.markdown(
        """
        <h1>🖼️ Sample Retrievals Gallery</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Browse example retrieval results from all three models side by side.
            Switch between models to visually compare retrieval quality.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Per-model tabs ----
    tab1, tab2, tab3 = st.tabs([
        "🏗️ Baseline (pretrained)",
        "🔧 Transfer Learning",
        "🏆 Siamese Network",
    ])

    model_images = [
        ("sanity_check_baseline_retrieval.png", tab1,
         "Baseline retrieval quality: Uses generic ImageNet features without fine-tuning.",
         "Baseline retrieval grid"),
        ("sanity_check_finetuned_retrieval.png", tab2,
         "Transfer learning retrieval quality: ResNet50 fine-tuned on category labels. Noticeably better alignment.",
         "Transfer Learning retrieval grid"),
        ("sanity_check_siamese_retrieval.png", tab3,
         "Siamese Network retrieval quality: Trained with triplet loss for metric learning. Best visual consistency.",
         "Siamese Network retrieval grid"),
    ]

    for img_file, tab, caption, alt in model_images:
        with tab:
            img_path = get_image_path(img_file)
            if img_path:
                st.image(img_path, use_container_width=True)
                st.markdown(
                    f'<p style="text-align: center; font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">{caption}</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.info(f"Image not found: {img_file}")

    # ---- Category-specific sample retrievals ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Sample Retrievals by Product Category")

    category_samples = [
        ("sample_retrieval_shirts.png", "Shirts — top retrievals"),
        ("sample_retrieval_shoes.png", "Shoes — top retrievals (from the initial 5-category evaluation)"),
        ("sample_retrieval_dresses.png", "Dresses — top retrievals"),
        ("sample_retrieval_tshirts_watches.png", "T-shirts & Watches — top retrievals"),
    ]

    for img_file, caption in category_samples:
        img_path = get_image_path(img_file)
        if img_path:
            st.image(img_path, use_container_width=True)
            st.markdown(
                f'<p style="text-align: center; font-size: 0.85rem; opacity: 0.7; margin-top: 0.3rem;">{caption}</p>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.15); 
                    border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h3>🔍 Key Observation</h3>
            <p style="opacity: 0.8;">
                The Siamese Network consistently retrieves items that are not only the same category 
                but also visually more similar in style, shape, and color — a direct result of 
                triplet-loss metric learning pulling similar items together in embedding space.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
