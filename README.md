<div align="center">

# 🎯 Visual Product Recommendation System

**Deep learning-powered visual similarity search for fashion products — no text, no tags, just pure visual intelligence.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![FAISS](https://img.shields.io/badge/FAISS-1.7+-0099E5?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jahanvi2005-29/Streamlit-Visual-Product-Recommendation-system)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/cloud)

---

## 🌐 Live Demo

> [Try the App](https://app-visual-appuct-recommendation-system-t3dnl2spqracg5kupebqmq.streamlit.app/)
>
> 
---

## 📋 Overview

Traditional product recommendation systems rely heavily on text metadata — titles, descriptions, and manually assigned tags. This approach breaks down when:

- **Text data is incomplete or missing** from the catalog
- **Products look similar but have different descriptions** (e.g., "sneakers" vs "athletic shoes")
- **Visual attributes matter more than text** (pattern, color, shape)
- **New products arrive** without proper tagging

**Our solution:** A purely visual approach that compares products by their appearance alone, using deep convolutional neural networks to generate image embeddings and FAISS-powered similarity search to find the closest matches — exactly like a visual search engine.

We benchmarked **three progressively stronger approaches** on a curated dataset of **1,199 fashion catalog images** across **4 product categories**:

| Model | Description | Precision@5 |
|-------|-------------|:-----------:|
| **Baseline** | Pretrained ResNet50 (ImageNet weights), no fine-tuning | 97.2% |
| **Transfer Learning** | ResNet50 fine-tuned on product categories | 99.0% |
| **🏆 Siamese Network** | Custom 128-dim embedding trained with triplet loss | **99.7%** |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Live Recommendation** | Upload any fashion image and get real-time similar product recommendations via FAISS-powered similarity search |
| 🧠 **Three AI Models** | Compare Baseline ResNet50, Transfer Learning, and Siamese Network side-by-side |
| 🖼️ **Visual Retrieval Gallery** | Browse pre-computed retrievals for sample query images |
| 🔬 **Embedding Space Explorer** | Visualize the learned 128-dim embedding space with PCA / t-SNE projections |
| ⚔️ **Interactive Model Showdown** | Side-by-side comparison of model outputs with image sliders |
| ❌ **Error Analysis** | Explore failure cases where the model misclassified similar products |
| 📐 **FAISS Search Benchmark** | Live comparison of exact (FlatIP) vs approximate (IVFFlat) nearest neighbor search |
| ⚡ **Performance Dashboard** | End-to-end latency breakdown and dataset distribution analytics |
| 🌓 **Dark/Light Theme** | Premium glassmorphism UI with ambient lighting effects and smooth animations |
| 📱 **Responsive Design** | Fully responsive layout optimized for desktop and mobile |

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Programming Language** | ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) |
| **Deep Learning** | ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11+-FF6F00?logo=tensorflow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-D00000?logo=keras&logoColor=white) |
| **Similarity Search** | ![FAISS](https://img.shields.io/badge/FAISS-1.7+-0099E5) |
| **Web Framework** | ![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white) |
| **Data Processing** | ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white) |
| **Machine Learning** | ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white) |
| **Visualization** | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white) |
| **Image Processing** | ![Pillow](https://img.shields.io/badge/Pillow-10.0+-3776AB) |

---

## 📊 Key Results

### Final Benchmark

| Model | Precision@5 | Recall@5 | Embedding Time (s) |
|-------|:-----------:|:--------:|:------------------:|
| Baseline (pretrained) | 0.972 | 0.0163 | 165.4 |
| Transfer Learning | 0.990 | 0.0166 | 177.3 |
| **🏆 Siamese Network** | **0.997** | **0.0167** | **184.3** |

### Multi-K Performance (Precision / Recall)

| Model | K=5 | K=20 | K=50 |
|-------|:---:|:----:|:----:|
| Baseline | 0.972 / 0.016 | 0.946 / 0.063 | 0.913 / 0.153 |
| Transfer Learning | 0.990 / 0.017 | 0.988 / 0.066 | 0.988 / 0.165 |
| **Siamese Network** | **0.997 / 0.017** | **0.990 / 0.066** | **0.987 / 0.165** |

### Inference Latency

| Metric | Time |
|--------|:----:|
| Single-image embedding generation | 346.7 ms |
| Similarity search over 1,199 images (FAISS FlatIP) | 380.5 ms |
| **Total end-to-end query time** | **727.2 ms** |

### Dataset Composition

| Category | Image Count |
|----------|:-----------:|
| Watches | 300 |
| Tshirts | 300 |
| Dresses | 300 |
| Shirts | 299 |
| **Total** | **1,199** |

---

## 🧠 Architecture

```
Query Image (224×224)
       ↓
   CNN Backbone (ResNet50)
       ↓
   Embedding Vector (128-dim)
       ↓
   Cosine Similarity Search (FAISS)
       ↓
   Top-K Most Similar Products 🎯
```

The system uses **FAISS** (Facebook AI Similarity Search) for high-performance nearest neighbor search:
- **IndexFlatIP** — Exact brute-force search (cosine similarity via inner product on normalized vectors)
- **IndexIVFFlat** — Approximate search with inverted file indexing for >10× speedup at scale

---

## 📁 Project Structure

```
visual-product-recommender/
├── streamlit_app/              # Streamlit dashboard application
│   ├── app.py                  # Main entry point + sidebar navigation
│   ├── pages/                  # Application pages
│   │   ├── page_home.py        # Home / overview with metrics
│   │   ├── page_live_recommendation.py  # 🔥 Live image similarity search
│   │   ├── page_model_comparison.py     # Model performance comparison
│   │   ├── page_sample_retrievals.py    # Retrieval gallery
│   │   ├── page_model_showdown.py       # Interactive model showdown
│   │   ├── page_embedding_space.py      # PCA / t-SNE visualization
│   │   ├── page_error_case.py           # Error analysis
│   │   ├── page_benchmark.py            # FAISS search benchmark
│   │   ├── page_performance.py          # Performance & latency metrics
│   │   └── page_about.py                # About / credits
│   └── utils/                 # Utility modules
│       ├── components.py      # Reusable UI components
│       ├── data_loader.py     # Data loading with caching
│       ├── inference.py       # Live inference pipeline
│       └── theme.py           # Premium dark/light theme system
├── data/                      # CSV evaluation results
│   ├── final_comparison.csv   # Final model benchmark scores
│   ├── multi_k_comparison.csv # Multi-K precision/recall
│   ├── dataset_summary.csv    # Category image counts
│   ├── inference_latency.csv  # Latency breakdown
│   ├── training_history.csv   # Training curves data
│   ├── error_case_example.csv # Error case metadata
│   └── fashion_subset_manifest.csv  # Image manifest
├── models/                    # Pre-trained models & embeddings
│   ├── siamese_embedding_model.h5  # Trained Siamese network
│   ├── siamese_embeddings.npy      # 1,199 × 128-dim embeddings
│   ├── baseline_embeddings.npy     # Baseline ResNet50 embeddings
│   └── synthetic_*.npy             # Synthetic vectors for scaling tests
├── catalog/                   # Fashion product catalog images
│   ├── Watches/
│   ├── Tshirts/
│   ├── Dresses/
│   └── Shirts/
├── images/                    # Static visualization images
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version for Streamlit Cloud
├── start_app.py               # Local convenience launcher
└── .streamlit/config.toml     # Streamlit configuration
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/jahanvi2005-29/Streamlit-Visual-Product-Recommendation-system.git
cd Streamlit-Visual-Product-Recommendation-system

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt
```

---

## 🖥️ Running Locally

```bash
# Start the Streamlit application
streamlit run streamlit_app/app.py
```

Then open your browser to:
```
http://localhost:8501
```

### Alternative: Quick Launcher
```bash
python start_app.py
```
*(Windows only — launches on port 8524)*

> **Note:** All pre-trained models and embedding files are included directly in the repository under `models/`. No external downloads, API keys, or cloud services are required. FAISS indices are built and cached automatically on first run.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **"New app"** → select this repository
4. Set the **Main file path** to:
   ```
   streamlit_app/app.py
   ```
5. Click **"Deploy"**

The deployment will automatically:
- Install dependencies from `requirements.txt`
- Use Python 3.10 (pinned via `runtime.txt`)
- Load pre-trained models and embeddings from the `models/` directory
- Build FAISS indices on first run

> **Note:** Total repository size is approximately 102 MB (including the .h5 model file and .npy embeddings), well within Streamlit Cloud's 1 GB deployment limit.

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=streamlit_app -v
```

---

## 📄 Model & Data Notes

- **Models & Embeddings:** All pre-trained models (`.h5`) and pre-computed embeddings (`.npy`) are stored **in-repository** under `models/`. No external hosting required.
- **FAISS Indices:** Built and cached automatically on first app launch (`.faiss` files are gitignored).
- **Dataset:** Catalog images are stored under `catalog/` organized by category (Shirts, Dresses, Tshirts, Watches).
- **Static Results:** All evaluation CSV files and visualization images are pre-computed from the training notebook and stored in `data/` and `images/`.

---

## 👩‍💻 Author

**Jahanvi Gupta** — Built as part of an internship at **Celebal Technologies**.

---

## 📬 Contact & Links

- **GitHub Repository:** [https://github.com/jahanvi2005-29/Streamlit-Visual-Product-Recommendation-system](https://github.com/jahanvi2005-29/Streamlit-Visual-Product-Recommendation-system)
- **Live Demo:** [Streamlit Community Cloud](https://YOUR-APP-URL.streamlit.app) *(Update URL after deployment)*
- **Local Development:** `http://localhost:8501`

---

<div align="center">
    <sub>Built with ❤️ using <a href="https://streamlit.io">Streamlit</a>, <a href="https://tensorflow.org">TensorFlow</a>, and <a href="https://github.com/facebookresearch/faiss">FAISS</a></sub>
    <br>
    <sub>© 2026 Celebal Technologies</sub>
</div>
