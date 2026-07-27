<div align="center">

# 🎯 Visual Product Recommendation System

**Finding visually similar fashion products using deep learning — no text, no tags, no metadata.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![FAISS](https://img.shields.io/badge/FAISS-1.7+-0099E5?style=for-the-badge)](https://github.com/facebookresearch/faiss)

</div>

---

## 📋 Problem & Approach

Traditional product recommendation systems rely heavily on text metadata — titles, descriptions, and manually assigned tags. This approach breaks down when:

- **Text data is incomplete or missing** from the catalog
- **Products look similar but have different descriptions** (e.g., "sneakers" vs "athletic shoes")
- **Visual attributes matter more than text** (pattern, color, shape)
- **New products arrive** without proper tagging

**Our solution:** A purely visual approach that compares products by their appearance alone, using deep convolutional neural networks to generate image embeddings and cosine similarity to find the closest matches — exactly like a visual search engine.

### Three Models Benchmarked

| Model | Description |
|-------|------------|
| **Baseline** | Pretrained ResNet50 (ImageNet weights), no fine-tuning. Features extracted from the penultimate layer. |
| **Transfer Learning** | ResNet50 fine-tuned on the 4 product categories. Adapts pre-trained features to the fashion domain. |
| **🏆 Siamese Network** | Custom 128-dim embedding network trained with triplet loss. Learns a specialized metric space where visually similar products naturally cluster together. |

---

## 📊 Key Results

### Final Benchmark

| Model | Precision@5 | Recall@5 | Embedding Time (s) |
|-------|:-----------:|:--------:|:------------------:|
| Baseline (pretrained) | 0.972 | 0.0163 | 165.4 |
| Transfer Learning | 0.990 | 0.0166 | 177.3 |
| **🏆 Siamese Network** | **0.997** | **0.0167** | **184.3** |

### Multi-K Performance

| Model | K=5 | K=20 | K=50 |
|-------|:---:|:----:|:----:|
| **Baseline** | 0.972 / 0.016 | 0.946 / 0.063 | 0.913 / 0.153 |
| **Transfer Learning** | 0.990 / 0.017 | 0.988 / 0.066 | 0.988 / 0.165 |
| **Siamese Network** | **0.997 / 0.017** | **0.990 / 0.066** | **0.987 / 0.165** |

*Format: Precision / Recall*

### Inference Latency

| Metric | Time |
|--------|:----:|
| Single-image embedding generation | 346.7 ms |
| Similarity search over 1,199 images (FAISS FlatIP) | 380.5 ms |
| **Total end-to-end query time** | **727.2 ms** |

### Dataset

| Category | Image Count |
|----------|:-----------:|
| Watches | 300 |
| Tshirts | 300 |
| Dresses | 300 |
| Shirts | 299 |
| **Total** | **1,199** |

Embedding dimension: **128** (for all models)

---

## 🧠 Architecture Flow

```
Query Image (224×224)
       ↓
   CNN Backbone (ResNet50)
       ↓
   Embedding Vector (128-dim)
       ↓
   Cosine Similarity vs Catalog (FAISS)
       ↓
   Top-K Most Similar Products 🎯
```

The system uses **FAISS** (Facebook AI Similarity Search) for lightning-fast nearest neighbor search:
- **IndexFlatIP** — Exact brute-force search (cosine similarity via inner product on normalized vectors)
- **IndexIVFFlat** — Approximate search with inverted file indexing for >10× speedup at scale

---

## 🚀 Features (Streamlit App)

The project includes a multi-page Streamlit dashboard with 10 interactive pages:

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, metrics, and architecture |
| 🎯 **Live Recommendation** | Upload any fashion image and get real-time similar product recommendations via FAISS |
| 📊 **Model Comparison** | Side-by-side comparison of all three models |
| 🖼️ **Retrieval Gallery** | Browse pre-computed retrievals for sample queries |
| ⚔️ **Model Showdown** | Interactive model comparison with image sliders |
| 🔬 **Embedding Space** | PCA / t-SNE visualization of the learned 128-dim space |
| ❌ **Error Analysis** | Explore failure cases and retrieval misses |
| 📐 **FAISS Benchmark** | Benchmark FlatIP vs IVFFlat speed and accuracy |
| ⚡ **Performance** | Scale benchmarks (1K, 10K, 100K synthetic vectors) |
| 👩‍💻 **About** | Project credits and technical details |

### UI Highlights
- 🎨 Premium dark/light theme with frosted glass (glassmorphism) design
- 🌌 Ambient background orbs and noise texture
- 🔄 Interactive sidebar navigation with theme toggle
- 📱 Responsive layout
- ⚡ FAISS-powered real-time similarity search

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **TensorFlow / Keras** | Deep learning — ResNet50 backbone, Siamese Network with triplet loss |
| **Streamlit** | Interactive web dashboard |
| **FAISS** | Fast approximate nearest neighbor search |
| **scikit-learn** | PCA, t-SNE visualization, evaluation metrics |
| **NumPy / pandas** | Data processing and numerical operations |
| **Plotly** | Interactive charts and visualizations |
| **Pillow** | Image preprocessing |

---

## 📁 Project Structure

```
visual-product-recommender/
├── streamlit_app/              # Streamlit dashboard
│   ├── app.py                  # Main entry point + sidebar navigation
│   ├── pages/
│   │   ├── page_home.py        # Home / overview page
│   │   ├── page_live_recommendation.py  # Live image similarity search
│   │   ├── page_model_comparison.py     # Model comparison
│   │   ├── page_sample_retrievals.py    # Retrieval gallery
│   │   ├── page_model_showdown.py       # Interactive model showdown
│   │   ├── page_embedding_space.py      # PCA / t-SNE visualization
│   │   ├── page_error_case.py           # Error analysis
│   │   ├── page_benchmark.py            # FAISS benchmark
│   │   ├── page_performance.py          # Scale performance
│   │   └── page_about.py                # About page
│   └── utils/
│       ├── components.py       # Reusable UI components
│       ├── data_loader.py      # Data loading with caching
│       ├── inference.py        # Live inference pipeline
│       └── theme.py            # Premium theme system
├── data/                       # CSV results + manifest
│   ├── final_comparison.csv
│   ├── multi_k_comparison.csv
│   ├── dataset_summary.csv
│   ├── inference_latency.csv
│   ├── training_history.csv
│   ├── error_case_example.csv
│   └── fashion_subset_manifest.csv
├── models/                     # Pre-trained models & embeddings
│   ├── siamese_embedding_model.h5   # Trained Siamese network (Keras)
│   ├── siamese_embeddings.npy       # Pre-computed 128-dim embeddings
│   ├── baseline_embeddings.npy      # Baseline ResNet50 embeddings
│   └── synthetic_*.npy              # Synthetic embeddings for scale testing
├── catalog/                    # Fashion product catalog images
├── tests/                      # Unit tests
├── requirements.txt
├── start_app.py                # Quick-start launcher
└── .streamlit/config.toml      # Streamlit configuration
```

---

## 🚦 How to Run Locally

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/jahanvi2005-29/Streamlit-Visual-Product-Recommendation-system.git
cd Streamlit-Visual-Product-Recommendation-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 4. Launch the Streamlit app
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`. You can also use the convenience launcher:

```bash
python start_app.py
```

> **Note:** The Siamese model (`siamese_embedding_model.h5`) and all embedding files (`.npy`) are included directly in the repository under `models/`. No external downloads or API keys are required. The FAISS indices are built and cached automatically on first run.

---

## 📦 Models & Embeddings

All pre-trained models and pre-computed embeddings are stored **in-repository** under the `models/` directory:

| File | Size | Description |
|------|:----:|-------------|
| `siamese_embedding_model.h5` | ~95 MB | Trained Siamese network (Keras `.h5` format) |
| `siamese_embeddings.npy` | ~490 KB | 1,199 × 128-dim Siamese embeddings |
| `baseline_embeddings.npy` | ~1.4 MB | 1,199 × 2048-dim baseline embeddings |
| `synthetic_1k.npy` | ~500 KB | 1,000 synthetic 128-dim vectors (FAISS benchmark) |
| `synthetic_10k.npy` | ~5 MB | 10,000 synthetic vectors |
| `synthetic_100k.npy` | ~50 MB | 100,000 synthetic vectors |

FAISS indices (`.faiss` files) are automatically built and cached on first use — no separate download needed.

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=streamlit_app -v
```

---

## 👩‍💻 Author

**Jahanvi Gupta** — Built as part of an internship at Celebal Technologies.

---

## 📄 License

This project is for educational and demonstration purposes.

---

<div align="center">
    <sub>Built with ❤️ using Streamlit, TensorFlow, and FAISS</sub>
</div>
