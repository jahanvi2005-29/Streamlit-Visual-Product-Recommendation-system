"""
Data loading utilities with Streamlit caching.
All CSV files, embeddings, and the manifest are loaded with @st.cache_data.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

# Base paths
# data_loader.py is at: streamlit_app/utils/data_loader.py
# Project root is 3 levels up
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = PROJECT_ROOT / "data"
IMAGES_DIR = PROJECT_ROOT / "images"
MODELS_DIR = PROJECT_ROOT / "models"
CATALOG_DIR = PROJECT_ROOT / "catalog"


@st.cache_data(show_spinner=False)
def load_final_comparison():
    """Load final model comparison data."""
    path = DATA_DIR / "final_comparison.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_multi_k_comparison():
    """Load multi-K comparison data."""
    path = DATA_DIR / "multi_k_comparison.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_dataset_summary():
    """Load dataset summary (category counts)."""
    path = DATA_DIR / "dataset_summary.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_inference_latency():
    """Load inference latency data."""
    path = DATA_DIR / "inference_latency.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_training_history():
    """Load training history data."""
    path = DATA_DIR / "training_history.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_error_case_example():
    """Load error case example data."""
    path = DATA_DIR / "error_case_example.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_manifest():
    """Load the image manifest CSV with corrected paths."""
    path = DATA_DIR / "fashion_subset_manifest.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    # Fix paths: /content/fashion_subset/Shirts/xxx.jpg → catalog/Shirts/xxx.jpg
    if "path" in df.columns:
        df["path"] = df["path"].apply(lambda p: "/".join(p.split("/")[-2:]))
        df["local_path"] = df["path"].apply(lambda p: str(CATALOG_DIR / p))
    return df


@st.cache_data(show_spinner=False)
def load_siamese_embeddings():
    """Load precomputed Siamese embeddings (1199 x 128)."""
    path = MODELS_DIR / "siamese_embeddings.npy"
    if not path.exists():
        return None
    return np.load(path)


@st.cache_data(show_spinner=False)
def load_baseline_embeddings():
    """Load precomputed baseline embeddings."""
    path = MODELS_DIR / "baseline_embeddings.npy"
    if not path.exists():
        return None
    return np.load(path)


@st.cache_data(show_spinner=False)
def load_synthetic_embeddings(size_k=100):
    """Load pre-generated synthetic embeddings at a given scale.
    
    Args:
        size_k: 1, 10, or 100 (thousands of vectors)
    """
    name = f"synthetic_{size_k}k.npy"
    path = MODELS_DIR / name
    if not path.exists():
        return None
    return np.load(path)


@st.cache_resource(show_spinner=True)
def load_faiss_index(embeddings_key="siamese", index_type="flat"):
    """
    Build (or load from disk) a FAISS index for fast nearest neighbor search.
    
    Indices are persisted to disk as <embeddings_key>_<index_type>.faiss in the
    models/ directory. On subsequent loads, the cached .faiss file is used directly
    instead of rebuilding from scratch — as long as the source .npy file hasn't
    changed (checked via file modification time).
    
    Supports two index types:
      - "flat": IndexFlatIP — brute-force inner product (exact search).
        Guarantees exact cosine similarity results. Best for datasets up to ~100K.
      - "ivf": IndexIVFFlat — inverted file index (approximate search).
        Uses k-means clustering for faster search at scale.
        nprobe (cells searched) is serialized alongside the index.
    
    All embeddings are L2-normalized before indexing, so inner product = cosine similarity.
    
    Args:
        embeddings_key: "siamese" or "baseline"
        index_type: "flat" (exact) or "ivf" (approximate)
    
    Returns:
        faiss.Index or None if embeddings not available
    """
    import faiss

    # Determine paths
    if embeddings_key == "siamese":
        embeddings_path = MODELS_DIR / "siamese_embeddings.npy"
        embeddings = load_siamese_embeddings()
    elif embeddings_key == "baseline":
        embeddings_path = MODELS_DIR / "baseline_embeddings.npy"
        embeddings = load_baseline_embeddings()
    else:
        return None

    if embeddings is None:
        return None

    faiss_path = MODELS_DIR / f"{embeddings_key}_{index_type}.faiss"

    # ---- Try loading from disk if the .faiss file is fresh ----
    if faiss_path.exists():
        source_mtime = embeddings_path.stat().st_mtime if embeddings_path.exists() else 0
        faiss_mtime = faiss_path.stat().st_mtime
        if faiss_mtime >= source_mtime:
            try:
                index = faiss.read_index(str(faiss_path))
                return index
            except Exception:
                pass  # Corrupted file — fall through to rebuild

    # ---- Build index from scratch ----
    d = embeddings.shape[1]
    n = embeddings.shape[0]

    # Normalize so inner product = cosine similarity
    emb = embeddings.astype(np.float32)
    faiss.normalize_L2(emb)

    if index_type == "flat":
        index = faiss.IndexFlatIP(d)
        index.add(emb)

    elif index_type == "ivf":
        # nlist: number of Voronoi cells. Using n // 50 ensures enough
        # training points for k-means (rule: need ≥ nlist × 39 points)
        nlist = max(1, min(25, n // 50))
        nprobe = min(nlist, 5)

        quantizer = faiss.IndexFlatIP(d)
        index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
        index.train(emb)
        index.add(emb)
        index.nprobe = nprobe

    else:
        return None

    # ---- Persist to disk so next load is instant ----
    try:
        faiss.write_index(index, str(faiss_path))
    except Exception:
        pass  # Non-critical — we still return the in-memory index

    return index


@st.cache_resource(show_spinner=True)
def load_siamese_model():
    """Load the trained Siamese embedding model (Keras)."""
    path = MODELS_DIR / "siamese_embedding_model.h5"
    if not path.exists():
        return None
    import tensorflow as tf
    try:
        model = tf.keras.models.load_model(str(path), compile=False)
        return model
    except Exception as e:
        st.warning(f"Could not load Siamese model: {e}")
        return None


@st.cache_resource(show_spinner=False)
def _load_npy_for_benchmark():
    """Pre-load Siamese embeddings for benchmark to avoid cache-data interference."""
    return load_siamese_embeddings()


def run_faiss_benchmark(n_queries=50, k_values=None, nprobe_values=None):
    """
    Benchmark FAISS FlatIP vs IVFFlat search speed and accuracy.
    
    Runs timed searches on the Siamese embedding dataset and returns
    a structured dict with per-query timing and accuracy data.
    
    Args:
        n_queries: Number of random queries to run for stable averages
        k_values: List of top-K values to test (default: [5, 20, 50])
        nprobe_values: List of nprobe values to test for IVF (default: [1, 2, 5, 10, 23])
    
    Returns:
        dict with summary stats, per-query results, and accuracy data
    """
    import faiss
    import time

    if k_values is None:
        k_values = [5, 20, 50]
    if nprobe_values is None:
        nprobe_values = [1, 2, 5, 10, 23]

    embeddings = _load_npy_for_benchmark()
    if embeddings is None:
        return None

    emb = embeddings.astype(np.float32)
    faiss.normalize_L2(emb)
    n, d = emb.shape

    rng = np.random.RandomState(42)
    query_indices = rng.choice(n, min(n_queries, n), replace=False)
    queries = emb[query_indices]

    # ---- Build Flat index (for baseline and accuracy reference) ----
    t0 = time.time()
    flat_index = faiss.IndexFlatIP(d)
    flat_index.add(emb)
    flat_build_ms = (time.time() - t0) * 1000

    # ---- Build IVF index with max nprobe for accuracy reference ----
    nlist = max(1, min(25, n // 50))
    quantizer = faiss.IndexFlatIP(d)
    ivf_index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
    t1 = time.time()
    ivf_index.train(emb)
    ivf_index.add(emb)
    ivf_build_ms = (time.time() - t1) * 1000
    ivf_index.nprobe = min(nlist, 23)

    # ---- Run Flat benchmark ----
    flat_results = {k: [] for k in k_values}
    flat_query_times = []
    for q in queries:
        q_2d = q.reshape(1, -1)
        t = time.time()
        d_i, i_i = flat_index.search(q_2d, max(k_values))
        elapsed = (time.time() - t) * 1000
        flat_query_times.append(elapsed)
        for k in k_values:
            flat_results[k].append({
                "indices": i_i[0][:k].tolist(),
                "scores": d_i[0][:k].tolist(),
            })

    # ---- Run IVF benchmark for each nprobe ----
    ivf_data = {}
    for nprobe in nprobe_values:
        ivf_index.nprobe = nprobe
        query_times = []
        results = {k: [] for k in k_values}
        for q in queries:
            q_2d = q.reshape(1, -1)
            t = time.time()
            d_i, i_i = ivf_index.search(q_2d, max(k_values))
            elapsed = (time.time() - t) * 1000
            query_times.append(elapsed)
            for k in k_values:
                results[k].append({
                    "indices": i_i[0][:k].tolist(),
                    "scores": d_i[0][:k].tolist(),
                })

        # Compute accuracy vs Flat for each K
        accuracy = {}
        for k in k_values:
            correct = 0
            total = 0
            for qi in range(len(queries)):
                flat_set = set(flat_results[k][qi]["indices"])
                ivf_set = set(results[k][qi]["indices"])
                correct += len(flat_set & ivf_set)
                total += k
            accuracy[k] = correct / total if total > 0 else 0

        ivf_data[nprobe] = {
            "query_times_ms": query_times,
            "avg_time_ms": float(np.mean(query_times)),
            "std_time_ms": float(np.std(query_times)),
            "results": results,
            "accuracy": accuracy,
        }

    return {
        "n": n,
        "d": d,
        "nlist": nlist,
        "n_queries": len(queries),
        "k_values": k_values,
        "nprobe_values": nprobe_values,
        "flat_build_ms": flat_build_ms,
        "ivf_build_ms": ivf_build_ms,
        "flat": {
            "query_times_ms": flat_query_times,
            "avg_time_ms": float(np.mean(flat_query_times)),
            "std_time_ms": float(np.std(flat_query_times)),
            "results": flat_results,
        },
        "ivf": ivf_data,
    }


def run_scale_benchmark(sizes=None, n_queries=50):
    """
    Benchmark FlatIP vs IVFFlat search at multiple synthetic scales.
    
    Builds FAISS indices at each scale (e.g. 1K, 10K, 100K vectors)
    and measures build time + search time for both index types.
    
    Args:
        sizes: List of sizes in thousands, e.g. [1, 10, 100]
        n_queries: Number of random queries per scale
    
    Returns:
        dict with per-scale timing results or None on failure
    """
    import faiss
    import time

    if sizes is None:
        sizes = [1, 10, 100]

    # Pre-load all embeddings
    all_embs = {}
    for s in sizes:
        name = f"synthetic_{s}k.npy"
        path = MODELS_DIR / name
        if not path.exists():
            print(f"Missing: {path}")
            return None
        all_embs[s] = np.load(path).astype(np.float32)
        # Already normalized from generation, but double-check
        faiss.normalize_L2(all_embs[s])

    rng = np.random.RandomState(42)
    results = {}

    for s in sizes:
        emb = all_embs[s]
        n, d = emb.shape

        # Pick query indices (exclude from index building? not needed — we just measure speed)
        q_idx = rng.choice(n, min(n_queries, n), replace=False)
        queries = emb[q_idx]

        # ---- Build FlatIP ----
        t0 = time.time()
        flat = faiss.IndexFlatIP(d)
        flat.add(emb)
        flat_build = (time.time() - t0) * 1000

        # Time Flat searches
        flat_times = []
        for q in queries:
            t = time.time()
            flat.search(q.reshape(1, -1), 10)
            flat_times.append((time.time() - t) * 1000)

        # ---- Build IVFFlat ----
        nlist = max(1, min(int(n ** 0.5), 200))
        quantizer = faiss.IndexFlatIP(d)
        ivf = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
        t0 = time.time()
        ivf.train(emb)
        ivf.add(emb)
        ivf_build = (time.time() - t0) * 1000
        ivf.nprobe = min(nlist, 10)

        # Time IVF searches
        ivf_times = []
        for q in queries:
            t = time.time()
            ivf.search(q.reshape(1, -1), 10)
            ivf_times.append((time.time() - t) * 1000)

        results[s] = {
            "n": n,
            "d": d,
            "nlist": nlist,
            "flat_build_ms": round(flat_build, 2),
            "ivf_build_ms": round(ivf_build, 2),
            "flat_search_avg_ms": round(float(np.mean(flat_times)), 4),
            "flat_search_std_ms": round(float(np.std(flat_times)), 4),
            "ivf_search_avg_ms": round(float(np.mean(ivf_times)), 4),
            "ivf_search_std_ms": round(float(np.std(ivf_times)), 4),
            "speedup": round(float(np.mean(flat_times)) / float(np.mean(ivf_times)), 1),
        }

    return results


def get_image_path(filename):
    """Get the full path to a static result image."""
    path = IMAGES_DIR / filename
    if path.exists():
        return str(path)
    return None


def list_sample_query_images():
    """List available sample query images from catalog for the demo."""
    samples = {}
    categories = ["Shirts", "Dresses", "Tshirts", "Watches"]
    for cat in categories:
        cat_dir = CATALOG_DIR / cat
        if cat_dir.exists():
            images = sorted([str(f) for f in cat_dir.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")])
            if images:
                samples[cat] = images[:4]
    return samples
