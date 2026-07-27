"""
Page 2 — Live Recommendation
Real-time visual similarity search using the trained Siamese embedding model.
Includes a side-by-side comparison mode to visually compare query vs results.
"""

import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import os

from utils.theme import get_theme
from utils.data_loader import list_sample_query_images, PROJECT_ROOT, get_image_path
from utils.inference import run_live_inference


def _img_to_data_uri(img, max_size=200):
    """Convert a PIL Image to a base64 data URI, resized to fit."""
    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def _render_compare_mode(query_image, results_list):
    """Render results in side-by-side comparison mode."""
    query_uri = _img_to_data_uri(query_image.copy(), max_size=200)

    for item in results_list:
        rank = item["rank"]
        score = item["similarity"]
        score_pct = max(0, min(100, score * 100))
        cat = item["category"]
        img_path = item["image_path"]

        # Load result image if available
        result_uri = None
        if os.path.exists(img_path):
            result_img = Image.open(img_path)
            result_uri = _img_to_data_uri(result_img, max_size=200)

        if result_uri:
            st.markdown(
                f"""
                <div class="compare-row">
                    <div class="compare-side">
                        <img src="{query_uri}" alt="Query image">
                        <div class="compare-side-label">Query</div>
                    </div>
                    <div class="compare-vs-divider">
                        <div class="compare-vs-badge">VS</div>
                    </div>
                    <div class="compare-side">
                        <img src="{result_uri}" alt="Result #{rank}">
                        <div class="compare-side-label">Result #{rank}</div>
                    </div>
                    <div style="flex: 0 0 140px; padding-left: 0.5rem; display: flex; flex-direction: column; justify-content: center;">
                        <div class="compare-info">
                            <span class="compare-rank">#{rank}</span>
                            <span style="opacity:0.6;"> · </span>
                            <span class="category-tag" style="font-size:0.75rem;">#{cat}</span>
                        </div>
                        <div style="margin-top:0.4rem;">
                            <div class="score-label" style="font-size:0.8rem;">Match: {score:.4f}</div>
                            <div class="sim-bar">
                                <div class="sim-bar-fill" style="width: {score_pct}%;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_grid_mode(results_list):
    """Render results in the default grid layout."""
    n_cols = min(5, len(results_list))
    rows = (len(results_list) + n_cols - 1) // n_cols

    for row_idx in range(rows):
        cols = st.columns(n_cols)
        for col_idx in range(n_cols):
            item_idx = row_idx * n_cols + col_idx
            if item_idx < len(results_list):
                item = results_list[item_idx]
                with cols[col_idx]:
                    img_path = item["image_path"]
                    if os.path.exists(img_path):
                        result_img = Image.open(img_path)
                        st.image(result_img, use_container_width=True)

                    score = item["similarity"]
                    score_pct = max(0, min(100, score * 100))
                    cat = item["category"]

                    st.markdown(
                        f"""
                        <div class="result-item">
                            <div class="category-tag">#{cat}</div>
                            <div class="score-label">Match: {score:.4f}</div>
                            <div class="sim-bar">
                                <div class="sim-bar-fill" style="width: {score_pct}%;"></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def show():
    theme = get_theme()

    st.markdown(
        """
        <h1>🎯 Live Recommendation</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Upload a fashion product image, take a photo, or select a sample to find visually similar items 
            from our catalog in real time.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Controls ----
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        input_method = st.radio(
            "Choose input method:",
            ["Upload an image", "Take a Photo", "Pick a sample catalog image"],
            horizontal=True,
        )

    with col2:
        model_choice = st.selectbox(
            "Retrieval model:",
            ["Siamese Network", "Baseline", "Transfer Learning"],
            help="Siamese Network is the best-performing model. Baseline and Transfer Learning use precomputed results.",
        )

    with col3:
        top_k = st.slider("Number of results (K):", 5, 50, 20, step=5)

    # ---- QA Search mode toggle ----
    search_mode = st.radio(
        "Search mode:",
        ["Exact (FlatIP)", "Approximate (IVF)"],
        horizontal=True,
        index=0,
        key="search_mode_radio",
        help="Exact (FlatIP) = 100% accurate brute-force. Approximate (IVF) = faster at scale via inverted file index.",
    )
    # Normalize to "flat" or "ivf" for the inference engine
    search_mode_key = "ivf" if "IVF" in search_mode else "flat"

    # ---- Image Input ----
    uploaded_file = None
    selected_sample = None
    camera_file = None
    query_image = None

    if input_method == "Upload an image":
        uploaded_file = st.file_uploader(
            "Choose a fashion product image...",
            type=["jpg", "jpeg", "png"],
            help="Upload any fashion product image (JPG or PNG)",
        )
    elif input_method == "Pick a sample catalog image":
        samples = list_sample_query_images()
        if samples:
            categories = list(samples.keys())
            selected_category = st.selectbox("Select a category:", categories)

            if selected_category and selected_category in samples:
                cat_images = samples[selected_category]
                st.markdown(
                    f"<p style='font-size:0.85rem; opacity:0.7;'>Click a thumbnail to use it as the query:</p>",
                    unsafe_allow_html=True,
                )

                img_cols = st.columns(len(cat_images))
                for i, img_path in enumerate(cat_images):
                    with img_cols[i]:
                        img = Image.open(img_path)
                        img.thumbnail((150, 150))
                        if st.button(f"Select", key=f"sample_{i}"):
                            st.session_state["selected_query_path"] = img_path
                            st.rerun()
                        st.image(img, use_container_width=True)

                if "selected_query_path" in st.session_state:
                    selected_path = st.session_state["selected_query_path"]
                    if os.path.exists(selected_path):
                        with open(selected_path, "rb") as f:
                            selected_sample = f.read()
                        query_image = Image.open(selected_path)
                        st.success(f"✅ Selected: {os.path.basename(selected_path)}")
    else:  # "Take a Photo"
        camera_file = st.camera_input(
            "Capture a fashion product photo",
            help="Use your device camera to capture a fashion product. Works on desktop (webcam) and mobile (phone camera).",
        )
        if camera_file is None:
            st.markdown(
                "<p style='opacity: 0.6; font-size: 0.95rem;'>"
                "📸 Point your device camera at a fashion product and click the "
                "<strong>capture button</strong> above to take a photo."
                "</p>",
                unsafe_allow_html=True,
            )

    # ---- Process query ----
    if uploaded_file is not None:
        query_bytes = uploaded_file.getvalue()
        query_image = Image.open(uploaded_file)
    elif selected_sample is not None:
        query_bytes = selected_sample
    elif camera_file is not None:
        query_bytes = camera_file.getvalue()
        query_image = Image.open(camera_file)
    else:
        query_bytes = None

    # ---- Run Inference ----
    if query_bytes is not None:
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("### Query Image")
            if query_image:
                st.image(query_image, use_container_width=True)

        with col_right:
            st.markdown("### Results")

            with st.spinner("🔍 Generating embedding & searching catalog..."):
                result = run_live_inference(query_bytes, model_name=model_choice, top_k=top_k, search_mode=search_mode_key)

            if result["success"]:
                timing = result["timing"]
                total_ms = timing.get("total_ms", 0)
                embed_ms = timing.get("embedding_ms", 0)
                search_ms = timing.get("search_ms", 0)

                search_mode_display = result.get("search_mode", "flat")
                search_label = "Exact (FlatIP)" if search_mode_display == "flat" else "Approximate (IVF)"
                search_badge_color = "rgba(16,185,129,0.15)" if search_mode_display == "flat" else "rgba(251,191,36,0.15)"
                search_badge_border = "rgba(16,185,129,0.25)" if search_mode_display == "flat" else "rgba(251,191,36,0.25)"

                st.markdown(
                    f"""
                    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
                        <div style="background: rgba(108,99,255,0.1); padding: 0.5rem 1rem; border-radius: 8px; 
                                    border: 1px solid rgba(108,99,255,0.2); font-size: 0.85rem;">
                            ⏱ <strong>Total:</strong> {total_ms:.1f} ms
                        </div>
                        <div style="background: rgba(108,99,255,0.08); padding: 0.5rem 1rem; border-radius: 8px; 
                                    border: 1px solid rgba(108,99,255,0.15); font-size: 0.85rem;">
                            🧠 <strong>Embedding:</strong> {embed_ms:.1f} ms
                        </div>
                        <div style="background: rgba(108,99,255,0.08); padding: 0.5rem 1rem; border-radius: 8px; 
                                    border: 1px solid rgba(108,99,255,0.15); font-size: 0.85rem;">
                            🔍 <strong>Search:</strong> {search_ms:.1f} ms
                        </div>
                        <div style="background: {search_badge_color}; padding: 0.5rem 1rem; border-radius: 8px; 
                                    border: 1px solid {search_badge_border}; font-size: 0.85rem;">
                            📐 <strong>{search_label}</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                results_list = result["results"]
                if results_list:
                    # ---- Compare mode toggle ----
                    use_compare = st.checkbox(
                        "🔄 Enable side-by-side comparison",
                        key="compare_mode",
                        help="Toggle to compare each result side-by-side with your query image",
                    )

                    if use_compare and query_image:
                        _render_compare_mode(query_image, results_list)
                    else:
                        _render_grid_mode(results_list)
                else:
                    st.info("No results found.")
            else:
                st.warning(
                    f"⚠️ Live inference temporarily unavailable: {result.get('error', 'Unknown error')}. "
                    "Showing cached pre-computed results instead."
                )
                _show_fallback_results(model_choice)

    elif query_bytes is None:
        st.info("👆 Upload an image, take a photo, or select a sample to get started.")

    # ---- Info box ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    model_sizes = {
        "Siamese Network": (
            "✅ **Fully live** — uses the trained Siamese embedding model (128-dim) "
            "to generate a fresh embedding for your query image in real time."
        ),
        "Baseline": (
            "⚠️ **Pre-computed results only** — the baseline model runs on pre-generated "
            "ResNet50 embeddings. Live embedding generation falls back to the Siamese model."
        ),
        "Transfer Learning": (
            "⚠️ **Pre-computed results only** — the fine-tuned model weights are not "
            "available as a standalone .h5 file. Results shown are from the evaluation notebook."
        ),
    }

    with st.expander("ℹ️ About this page"):
        st.markdown(model_sizes.get(model_choice, ""))
        model_path = PROJECT_ROOT / "models" / "siamese_embedding_model.h5"
        size_mb = round(model_path.stat().st_size / (1024 * 1024)) if model_path.exists() else 0
        st.markdown(
            f"""
            **Model info:** The Siamese Network was trained with triplet loss over 3 epochs, 
            generating a 128-dimensional embedding space optimized for visual similarity.
            The .h5 model file is ~{size_mb} MB and is cached after first load.<br><br>
            💡 <strong>Tip:</strong> Enable <em>side-by-side comparison</em> mode to visually 
            compare each result directly against your query image.
            """
        )


def _show_fallback_results(model_choice):
    """Show static fallback images when live inference fails."""
    fallback_map = {
        "Siamese Network": "sanity_check_siamese_retrieval.png",
        "Baseline": "sanity_check_baseline_retrieval.png",
        "Transfer Learning": "sanity_check_finetuned_retrieval.png",
    }

    img_file = fallback_map.get(model_choice)
    if img_file:
        img_path = get_image_path(img_file)
        if img_path:
            st.image(img_path, use_container_width=True)
            st.caption(f"Cached retrieval grid for {model_choice}")
