"""
Page 8 — Performance & Latency Benchmarking
Inference latency breakdown and dataset distribution charts.
"""

import time
import streamlit as st
import plotly.express as px
from utils.theme import get_theme
from utils.data_loader import load_inference_latency, load_dataset_summary, load_final_comparison, load_faiss_index


def _run_live_search_benchmark(index_type="flat", n_queries=20, top_k=20):
    """Load a FAISS index and run a quick timed search benchmark."""
    import faiss
    import numpy as np

    index = load_faiss_index("siamese", index_type=index_type)
    if index is None:
        return None

    # Generate random normalized query vectors
    rng = np.random.RandomState(99)
    queries = rng.randn(n_queries, 128).astype(np.float32)
    faiss.normalize_L2(queries)

    times = []
    for q in queries:
        t0 = time.time()
        index.search(q.reshape(1, -1), top_k)
        times.append((time.time() - t0) * 1000)

    return {
        "avg_ms": float(np.mean(times)),
        "std_ms": float(np.std(times)),
        "min_ms": float(np.min(times)),
        "max_ms": float(np.max(times)),
        "n_queries": n_queries,
    }


def show():
    theme = get_theme()

    st.markdown(
        """
        <h1>⚡ Performance & Latency</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Production-readiness benchmarking: how fast can we generate an embedding, 
            search the catalog, and return results?
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- FAISS Search Mode Toggle ----
    col_mode, col_run = st.columns([3, 1])
    with col_mode:
        search_mode = st.radio(
            "Search mode:",
            ["Exact (FlatIP)", "Approximate (IVF)"],
            horizontal=True,
            index=0,
            key="perf_search_mode",
            help="Exact (FlatIP) = 100% accurate brute-force. Approximate (IVF) = faster at scale via inverted file index.",
        )
    with col_run:
        st.markdown("<br>", unsafe_allow_html=True)
        run_bench = st.button("🔍 Run Search Benchmark", type="primary", use_container_width=True)

    search_mode_key = "ivf" if "IVF" in search_mode else "flat"
    search_label = "Approximate (IVF)" if search_mode_key == "ivf" else "Exact (FlatIP)"
    search_badge_color = "rgba(251,191,36,0.15)" if search_mode_key == "ivf" else "rgba(16,185,129,0.15)"
    search_badge_border = "rgba(251,191,36,0.25)" if search_mode_key == "ivf" else "rgba(16,185,129,0.25)"

    # ---- Live benchmark results ----
    live_bench = None
    if run_bench:
        with st.spinner(f"Running search benchmark with {search_label}..."):
            live_bench = _run_live_search_benchmark(index_type=search_mode_key)

    # ---- Inference Latency ----
    latency_df = load_inference_latency()
    if latency_df is not None:
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("### Latency Breakdown")

            fig = px.bar(
                latency_df,
                y="Metric",
                x="Value_ms",
                orientation="h",
                color="Metric",
                color_discrete_map={
                    "Single-image embedding generation": "#6C63FF",
                    "Similarity search over 1199 images": "#8B83FF",
                    "Total end-to-end query time": "#FF6B9D",
                },
                text="Value_ms",
                labels={"Value_ms": "Time (ms)", "Metric": ""},
            )
            fig.update_traces(
                texttemplate='%{text:.1f} ms',
                textposition='outside',
                marker=dict(line=dict(width=0)),
            )
            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Time (milliseconds)",
                margin=dict(l=20, r=20, t=10, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=theme["text"], size=12),
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Key Takeaways")

            total_time = latency_df[latency_df["Metric"] == "Total end-to-end query time"]
            total_ms = total_time["Value_ms"].values[0] if not total_time.empty else 0
            embed_time = latency_df[latency_df["Metric"] == "Single-image embedding generation"]
            embed_ms = embed_time["Value_ms"].values[0] if not embed_time.empty else 0
            search_time = latency_df[latency_df["Metric"] == "Similarity search over 1199 images"]
            search_ms = search_time["Value_ms"].values[0] if not search_time.empty else 0

            st.markdown(
                f"""
                <div class="custom-card" style="text-align: center;">
                    <h3 style="font-size: 2.5rem; color: #6C63FF !important;">{total_ms:.0f} ms</h3>
                    <p style="opacity: 0.7;">End-to-end query time</p>
                </div>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                    <div class="custom-card" style="flex:1; text-align: center; padding: 1rem;">
                        <div style="font-size: 1.3rem; font-weight: 700;">{embed_ms:.0f} ms</div>
                        <div style="font-size: 0.75rem; opacity: 0.6;">Embedding</div>
                    </div>
                    <div class="custom-card" style="flex:1; text-align: center; padding: 1rem;">
                        <div style="font-size: 1.3rem; font-weight: 700;">{search_ms:.0f} ms</div>
                        <div style="font-size: 0.75rem; opacity: 0.6;">Search</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Active search mode badge
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.75rem;
                            background: {search_badge_color}; padding: 0.5rem 1rem; border-radius: 8px;
                            border: 1px solid {search_badge_border};">
                    <span style="font-size: 1.1rem;">📐</span>
                    <span style="font-size: 0.85rem;">
                        <strong>Active mode:</strong> {search_label}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Live benchmark results (if run)
            if live_bench is not None:
                st.markdown(
                    f"""
                    <div style="margin-top: 0.75rem; background: rgba(108,99,255,0.08); padding: 0.75rem 1rem;
                                border-radius: 8px; border: 1px solid rgba(108,99,255,0.15);">
                        <div style="font-size: 0.8rem; font-weight: 600; margin-bottom: 0.3rem;">⚡ Live Search Benchmark</div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                            <span>Avg: <strong>{live_bench['avg_ms']:.4f} ms</strong></span>
                            <span>Min: {live_bench['min_ms']:.3f} ms</span>
                            <span>Max: {live_bench['max_ms']:.3f} ms</span>
                        </div>
                        <div style="font-size: 0.7rem; opacity: 0.5; margin-top: 0.2rem;">
                            ({live_bench['n_queries']} random queries, top-{20})
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---- Dataset Distribution ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    df_summary = load_dataset_summary()
    if df_summary is not None:
        st.markdown("### Dataset Distribution")

        col1, col2 = st.columns([2, 1])

        with col1:
            fig2 = px.pie(
                df_summary,
                names="Category",
                values="Image_Count",
                color="Category",
                color_discrete_map={
                    "Watches": "#6C63FF",
                    "Tshirts": "#10B981",
                    "Dresses": "#F59E0B",
                    "Shirts": "#EF4444",
                },
                hole=0.4,
            )
            fig2.update_traces(
                textposition='outside',
                textinfo='label+percent',
                marker=dict(line=dict(color=theme["bg"], width=2)),
                hovertemplate="<b>%{label}</b><br>%{value} images<br>%{percent}",
            )
            fig2.update_layout(
                height=400,
                showlegend=False,
                margin=dict(l=20, r=20, t=10, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=theme["text"], size=12),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            total = df_summary["Image_Count"].sum()
            st.markdown(
                f"""
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #6C63FF;">{total}</div>
                    <div style="font-size: 0.9rem; opacity: 0.7;">Total Images</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for _, row in df_summary.iterrows():
                pct = row["Image_Count"] / total * 100
                st.markdown(
                    f"""
                    <div style="margin-top: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                            <span>{row['Category']}</span>
                            <span style="font-weight: 600;">{row['Image_Count']}</span>
                        </div>
                        <div class="sim-bar">
                            <div class="sim-bar-fill" style="width: {pct}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Dataset summary not found in data/ folder.")

    # ---- Model Comparison ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Embedding Time Comparison")

    df_final = load_final_comparison()
    if df_final is not None:
        fig3 = px.bar(
            df_final,
            x="Model",
            y="Embedding_time_seconds",
            color="Model",
            color_discrete_map={
                "Baseline (pretrained)": "#6B7280",
                "Transfer Learning": "#8B83FF",
                "Siamese Network": "#6C63FF",
            },
            text="Embedding_time_seconds",
            labels={"Embedding_time_seconds": "Time (seconds)", "Model": ""},
        )
        fig3.update_traces(texttemplate='%{text:.1f}s', textposition='outside')
        fig3.update_layout(
            height=350,
            showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown(
            """
            <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.15); 
                        border-radius: 12px; padding: 1.2rem;">
                <p style="margin: 0; opacity: 0.85;">
                    ⏱ <strong>Note:</strong> Embedding time is the total time to generate embeddings for 
                    <strong>all 1,199 catalog images</strong> (not a single query). The Siamese Network 
                    takes slightly longer due to its custom architecture, but the difference is marginal 
                    (~19s) and well worth the precision gain.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
