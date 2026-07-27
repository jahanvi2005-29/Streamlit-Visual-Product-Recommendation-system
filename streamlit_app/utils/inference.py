"""
Live inference engine for the Visual Product Recommendation System.
Handles image preprocessing, embedding generation, cosine similarity search,
and graceful fallbacks when models are unavailable.
"""

import time
import numpy as np
import streamlit as st
from PIL import Image
import io

from utils.data_loader import (
    load_siamese_model,
    load_siamese_embeddings,
    load_manifest,
    load_faiss_index,
)


def preprocess_image(image_bytes, target_size=(224, 224)):
    """
    Preprocess an uploaded image for the Siamese embedding model.
    Uses ResNet50's preprocess_input internally.
    """
    try:
        from tensorflow.keras.applications.resnet50 import preprocess_input
        from tensorflow.keras.preprocessing import image as tf_image

        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert("RGB")
        img = img.resize(target_size)
        img_array = tf_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    except Exception as e:
        st.error(f"Image preprocessing failed: {e}")
        return None


@st.cache_data(show_spinner=False)
def generate_embedding(_model, img_array):
    """Generate a 128-dimensional embedding from a preprocessed image."""
    try:
        embedding = _model.predict(img_array, verbose=0)
        # Normalize the embedding
        embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
        return embedding.flatten()
    except Exception as e:
        st.error(f"Embedding generation failed: {e}")
        return None


def search_with_faiss(query_embedding, faiss_index, top_k=20):
    """
    Search a FAISS index for the top-k most similar items.
    
    Args:
        query_embedding: 1D numpy array (normalized)
        faiss_index: FAISS IndexFlatIP (inner product = cosine sim for normalized vecs)
        top_k: Number of results to return
    
    Returns:
        (indices, scores) tuple, each sorted by similarity descending
    """
    if query_embedding is None or faiss_index is None:
        return None, None

    # FAISS expects (1, d) shape for single query
    query_2d = query_embedding.astype(np.float32).reshape(1, -1)
    
    # FAISS search returns (distances, indices)
    distances, indices = faiss_index.search(query_2d, min(top_k, faiss_index.ntotal))
    
    # For IndexFlatIP, distances = inner product = cosine similarity (since normalized)
    sorted_scores = distances[0]
    sorted_indices = indices[0]
    
    return sorted_indices, sorted_scores


def run_live_inference(image_bytes, model_name="Siamese Network", top_k=5, search_mode="flat"):
    """
    Run the full live inference pipeline.
    
    This function ONLY supports live inference for the Siamese Network model,
    because that's the only trained model available as a .h5 file. For Baseline
    and Transfer Learning models, it returns an error that triggers the UI to
    fall back to pre-computed static results.
    
    Args:
        image_bytes: Raw image bytes from upload
        model_name: "Siamese Network", "Baseline", or "Transfer Learning"
        top_k: Number of results to return
        search_mode: "flat" (exact, IndexFlatIP) or "ivf" (approximate, IndexIVFFlat)
    
    Returns:
        dict with results or error info
    """
    timing = {}
    result = {
        "success": False,
        "error": None,
        "timing": timing,
        "results": [],
        "query_image": None,
    }

    # Only Siamese Network supports live inference
    if model_name != "Siamese Network":
        result["error"] = (
            f"Live inference for '{model_name}' is not available. "
            "Only the Siamese Network model file (.h5) is provided. "
            "Showing pre-computed evaluation results instead."
        )
        return result

    # ---- Step 1: Preprocess image ----
    t0 = time.time()
    img_array = preprocess_image(image_bytes)
    if img_array is None:
        result["error"] = "Failed to preprocess image"
        return result
    timing["preprocessing_ms"] = (time.time() - t0) * 1000

    # ---- Step 2: Load Siamese model and generate embedding ----
    t1 = time.time()
    model = load_siamese_model()
    if model is None:
        result["error"] = "Siamese model not available"
        return result

    embedding = generate_embedding(model, img_array)

    if embedding is None:
        result["error"] = "Failed to generate embedding"
        return result
    timing["embedding_ms"] = (time.time() - t1) * 1000

    # ---- Step 3: FAISS-powered similarity search ----
    t2 = time.time()
    manifest = load_manifest()
    faiss_index = load_faiss_index("siamese", index_type=search_mode)

    if faiss_index is None or manifest is None:
        result["error"] = "FAISS index or manifest not available"
        return result

    sorted_indices, sorted_scores = search_with_faiss(embedding, faiss_index, top_k=top_k + 1)
    if sorted_indices is None:
        result["error"] = "FAISS similarity search failed"
        return result
    timing["search_ms"] = (time.time() - t2) * 1000

    # ---- Step 4: Look up results, excluding self-match if query is from catalog ----
    results = []
    for i in range(min(top_k + 1, len(sorted_indices))):
        idx = sorted_indices[i]
        score = float(sorted_scores[i])
        row = manifest.iloc[idx] if idx < len(manifest) else None
        if row is not None:
            cat = row.get("category", "Unknown")
            img_path = row.get("local_path", row.get("path", ""))
            results.append({
                "rank": i + 1,
                "index": int(idx),
                "category": cat,
                "image_path": img_path,
                "similarity": score,
            })

    # Trim to exactly top_k results (after potential self-match skip)
    result["success"] = True
    result["results"] = results[:top_k]
    result["timing"] = timing
    result["search_mode"] = search_mode
    timing["total_ms"] = (time.time() - t0) * 1000

    return result
