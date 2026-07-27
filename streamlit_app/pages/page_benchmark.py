"""
Page — FAISS Search Benchmark
Live timing comparison of FlatIP (exact) vs IVFFlat (approximate) search,
with adjustable nprobe and K parameters. Falls back to pre-computed
latency data if the live benchmark fails.
"""

import time
import streamlit as st
import plotly.express as px
from utils.theme import get_theme    # Lazy imports inside show() — see PEP 8 note: we import run_faiss_benchmark,
# load_inference_latency, and run_scale_benchmark inside the show() function
# so that if any function is missing for any reason, only this page degrades
# gracefully rather than crashing the entire app at import time.


def _show_fallback_benchmark():
    """Show pre-computed latency data when the live benchmark fails."""
    # Lazy import — only needed if the live benchmark fails
    from utils.data_loader import load_inference_latency

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📋 Pre-computed Latency Data")
    st.markdown(
        '<p style="font-size:0.95rem; opacity:0.8;">'
        "Showing cached inference latency results from the evaluation notebook.</p>",
        unsafe_allow_html=True,
    )

    latency_df = load_inference_latency()
    if latency_df is not None:
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
        fig.update_traces(texttemplate='%{text:.1f} ms', textposition='outside')
        fig.update_layout(
            height=300, showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8", size=12),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Cached latency data from data/inference_latency.csv")
    else:
        st.info("No cached latency data available.")


def show():
    # Lazy import so this page degrades gracefully if data_loader
    # is missing the benchmark function — avoids crashing the whole app
    import numpy as np
    from utils.data_loader import run_faiss_benchmark, run_scale_benchmark

    theme = get_theme()

    st.markdown(
        """
        <h1>📐 FAISS Search Benchmark</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Live comparison of exact (FlatIP) vs approximate (IVFFlat) nearest neighbor search 
            speed and accuracy on the Siamese embedding dataset.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Controls ----
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        n_queries = st.slider("Number of test queries:", 10, 200, 50, step=10,
                              help="More queries = more stable timing averages")

    with col2:
        max_k = st.selectbox("Max K for search:", [20, 50, 100], index=1,
                             help="Run benchmark at multiple K values up to this max")

    with col3:
        nprobe_options = st.multiselect(
            "IVF nprobe values to test:",
            [1, 2, 3, 5, 10, 15, 20, 23],
            default=[1, 5, 23],
            help="nprobe = number of clusters searched. Higher = more accurate but slower.",
        )
        if not nprobe_options:
            nprobe_options = [5]
            st.info("Defaulting to nprobe=5")

    k_values = [5, max_k] if max_k <= 20 else [5, 20, max_k]
    st.markdown(f"<p style='font-size:0.85rem; opacity:0.6;'>K values tested: {k_values}</p>",
                unsafe_allow_html=True)

    # ---- Run Benchmark ----
    if st.button("🚀 Run Benchmark", type="primary", use_container_width=True):
        try:
            with st.spinner(f"Running {n_queries} queries × {len(nprobe_options)} nprobe configs..."):
                t_start = time.time()
                data = run_faiss_benchmark(n_queries=n_queries, k_values=k_values,
                                           nprobe_values=nprobe_options)
                elapsed = time.time() - t_start
        except Exception as e:
            st.warning(
                f"⚠️ The FAISS benchmark function encountered an error: {e}. "
                "Showing pre-computed inference latency data instead."
            )
            _show_fallback_benchmark()
            return

        if data is None:
            st.error("Failed to run benchmark — embeddings not found.")
            return

        st.success(f"✅ Benchmark complete in {elapsed:.1f}s ({data['n_queries']} queries × {len(nprobe_options)} nprobe values)")

        # ---- Summary Stats ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Summary")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{data['n']}</div>
                    <div class="metric-label">Vectors</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{data['d']}</div>
                    <div class="metric-label">Dimensions</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{data['nlist']}</div>
                    <div class="metric-label">IVF Centroids</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{data['n_queries']}</div>
                    <div class="metric-label">Test Queries</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---- Build Times ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Index Build Time")
        build_df = {
            "Index": ["FlatIP (exact)", "IVFFlat (approximate)"],
            "Build Time (ms)": [round(data["flat_build_ms"], 2), round(data["ivf_build_ms"], 2)],
        }
        fig_build = px.bar(
            build_df, x="Index", y="Build Time (ms)", color="Index",
            color_discrete_map={"FlatIP (exact)": "#6C63FF", "IVFFlat (approximate)": "#8B83FF"},
            text="Build Time (ms)",
        )
        fig_build.update_traces(texttemplate='%{text:.1f} ms', textposition='outside')
        fig_build.update_layout(
            height=300, showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
        )
        st.plotly_chart(fig_build, use_container_width=True)

        # ---- Search Time Comparison ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Search Time Comparison")
        chart_data = []
        flat_avg = data["flat"]["avg_time_ms"]
        flat_std = data["flat"]["std_time_ms"]
        for np_val in nprobe_options:
            ivf = data["ivf"][np_val]
            chart_data.append({
                "Method": f"IVF (nprobe={np_val})",
                "Avg Time (ms)": round(ivf["avg_time_ms"], 4),
                "Std Time (ms)": round(ivf["std_time_ms"], 4),
            })
        chart_data.append({
            "Method": "FlatIP (exact)",
            "Avg Time (ms)": round(flat_avg, 4),
            "Std Time (ms)": round(flat_std, 4),
        })
        fig_speed = px.bar(
            chart_data, x="Method", y="Avg Time (ms)", color="Method",
            color_discrete_map={
                **{f"IVF (nprobe={np})": "#F59E0B" for np in nprobe_options},
                "FlatIP (exact)": "#6C63FF",
            },
            text="Avg Time (ms)", error_y="Std Time (ms)",
        )
        fig_speed.update_traces(texttemplate='%{text:.4f} ms', textposition='outside')
        fig_speed.update_layout(
            height=400, showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
            yaxis=dict(type="log", title="Time (ms, log scale)"),
        )
        st.plotly_chart(fig_speed, use_container_width=True)

        # ---- Accuracy vs nprobe ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Accuracy vs nprobe (Recall@K)")
        acc_data = []
        for np_val in nprobe_options:
            ivf = data["ivf"][np_val]
            for k in k_values:
                acc_data.append({
                    "nprobe": np_val, "K": k,
                    "Recall@K": round(ivf["accuracy"][k] * 100, 2),
                })
        fig_acc = px.line(
            acc_data, x="nprobe", y="Recall@K", color="K",
            markers=True, line_shape="spline",
            color_discrete_map={k: c for k, c in zip(k_values, ["#6C63FF", "#10B981", "#F59E0B"])},
            labels={"Recall@K": "Recall@K (%)", "nprobe": "nprobe (clusters searched)"},
        )
        fig_acc.update_traces(line=dict(width=3), marker=dict(size=10))
        fig_acc.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(range=[90, 100.5]),
        )
        fig_acc.add_hline(y=100, line_dash="dash", line_color="rgba(22,163,74,0.3)",
                          annotation_text="Perfect recall", annotation_position="bottom right")
        st.plotly_chart(fig_acc, use_container_width=True)

        # ---- Detailed Table ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Detailed Results")
        t = theme
        table_rows = ""
        for np_val in nprobe_options:
            ivf = data["ivf"][np_val]
            speedup = f"{flat_avg / ivf['avg_time_ms']:.1f}x" if ivf['avg_time_ms'] > 0 else "N/A"
            acc_str = " | ".join([f"@{k}={ivf['accuracy'][k]*100:.1f}%" for k in k_values])
            table_rows += f"""
            <tr>
                <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']};">IVF (nprobe={np_val})</td>
                <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">{ivf['avg_time_ms']:.4f}</td>
                <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">{speedup}</td>
                <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">{acc_str}</td>
            </tr>
            """
        table_rows += f"""
        <tr style="background: rgba(108,99,255,0.05);">
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; font-weight: 600;">FlatIP (exact)</td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; font-weight: 600;">{flat_avg:.4f}</td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center;">—</td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {t['border']}; text-align: center; color: #10B981;">100% (baseline)</td>
        </tr>
        """
        st.markdown(
            f"""
            <table style="width:100%; border-collapse: collapse; border-radius: 12px; overflow: hidden;">
                <thead>
                    <tr style="background: rgba(108,99,255,0.1);">
                        <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Method</th>
                        <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Avg Search (ms)</th>
                        <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Speedup</th>
                        <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Recall@K</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

        # ---- Projection to scale ----
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### Projected Performance at Scale")
        scale_factors = [data["n"], data["n"] * 10, data["n"] * 100, data["n"] * 1000]
        scale_labels = [f"{data['n']:,}", f"{data['n']*10:,}", f"{data['n']*100:,}", f"{data['n']*1_000:,}"]
        flat_proj = [round(flat_avg * (s / data["n"]), 1) for s in scale_factors]
        best_np = nprobe_options[0]
        ivf_base = data["ivf"][best_np]["avg_time_ms"]
        ivf_proj = [round(ivf_base * ((s / data["n"]) ** 0.5), 1) for s in scale_factors]
        proj_data = []
        for i, label in enumerate(scale_labels):
            proj_data.append({"Catalog Size": label, "FlatIP": flat_proj[i], "IVFFlat": ivf_proj[i]})
        fig_proj = px.line(
            proj_data, x="Catalog Size", y=["FlatIP", "IVFFlat"], markers=True,
            color_discrete_map={"FlatIP": "#6C63FF", "IVFFlat": "#F59E0B"},
            labels={"value": "Search Time (ms)", "variable": "Method"},
        )
        fig_proj.update_traces(line=dict(width=3), marker=dict(size=10))
        fig_proj.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(type="log", title="Projected Search Time (ms, log scale)"),
        )
        st.plotly_chart(fig_proj, use_container_width=True)

        st.markdown(
            f"""
            <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.15); 
                        border-radius: 12px; padding: 1.2rem;">
                <p style="margin: 0; opacity: 0.85;">
                    <strong>📈 Projection method:</strong> FlatIP scales linearly with catalog size 
                    O(n). IVFFlat scales approximately <strong>O(√n)</strong> with an inverted file 
                    index. At 1M+ vectors, IVF is orders of magnitude faster than brute-force while 
                    maintaining &gt;99% recall with the right nprobe setting.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ================================================================
        # REAL SCALING DEMO — Synthetic 1K / 10K / 100K
        # ================================================================
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("### 🧪 Real Scaling with Synthetic Data")

        scale_col1, scale_col2, scale_col3 = st.columns([1, 1, 2])
        with scale_col1:
            scale_nq = st.slider("Test queries per scale:", 10, 100, 50, step=10,
                                 key="scale_nq", help="Number of random queries at each scale")
        with scale_col2:
            scale_btn = st.button("🧪 Run Scaling Benchmark", type="primary",
                                  use_container_width=True, key="scale_btn")
        with scale_col3:
            st.markdown(
                "<p style='font-size:0.9rem; opacity:0.6; padding-top:0.6rem;'>"
                "Tests on 1K, 10K, and 100K synthetic 128-dim vectors to show "
                "real O(n) vs O(√n) scaling behavior.</p>",
                unsafe_allow_html=True,
            )

        if scale_btn:
            with st.spinner("Building FAISS indices at 1K, 10K, and 100K scale..."):
                raw = run_scale_benchmark(sizes=[1, 10, 100], n_queries=scale_nq)

            if raw is None:
                st.error("Synthetic embedding files not found. Run the generation script first.")
                st.code("python -c 'import numpy as np; ...'", language="python")
            else:
                st.success("Benchmark complete on synthetic data at 1K, 10K, and 100K scales.")

                # ---- Metric cards ----
                sc1, sc2, sc3 = st.columns(3)
                labels = {1: "1K Vectors", 10: "10K Vectors", 100: "100K Vectors"}
                for col, s in zip([sc1, sc2, sc3], [1, 10, 100]):
                    r = raw[s]
                    with col:
                        st.markdown(
                            f"""
                            <div class="custom-card" style="text-align: center;">
                                <div style="font-size:0.85rem; opacity:0.6;">{labels[s]}</div>
                                <div style="font-size:1.8rem; font-weight:800; color:#6C63FF;">
                                    {r['flat_search_avg_ms']:.2f}</div>
                                <div style="font-size:0.7rem; opacity:0.6;">FlatIP avg (ms)</div>
                                <div style="font-size:1.3rem; font-weight:700; margin-top:0.3rem; color:#F59E0B;">
                                    {r['ivf_search_avg_ms']:.4f}</div>
                                <div style="font-size:0.7rem; opacity:0.6;">IVFFlat avg (ms)</div>
                                <div style="margin-top:0.4rem; background:rgba(16,185,129,0.15);
                                            border-radius:6px; padding:0.25rem; font-size:0.85rem;
                                            font-weight:600; color:#10B981;">
                                    {r['speedup']}x faster</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                # ---- Log-log scaling chart ----
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
                st.markdown("### Search Time Scaling (Log-Log)")

                scales_labels = ["1K", "10K", "100K"]
                scale_values = [1_000, 10_000, 100_000]
                flat_avgs = [raw[s]["flat_search_avg_ms"] for s in [1, 10, 100]]
                ivf_avgs = [raw[s]["ivf_search_avg_ms"] for s in [1, 10, 100]]

                import plotly.graph_objects as go
                fig_scaling = go.Figure()
                fig_scaling.add_trace(go.Scatter(
                    x=scale_values, y=flat_avgs, mode="lines+markers",
                    name="FlatIP (brute-force)",
                    line=dict(color="#6C63FF", width=3),
                    marker=dict(size=12, symbol="circle"),
                ))
                fig_scaling.add_trace(go.Scatter(
                    x=scale_values, y=ivf_avgs, mode="lines+markers",
                    name="IVFFlat (approximate)",
                    line=dict(color="#F59E0B", width=3),
                    marker=dict(size=12, symbol="diamond"),
                ))

                # Annotation: O(n) reference slope
                ref_flat = flat_avgs[0] * (np.array(scale_values) / scale_values[0])
                fig_scaling.add_trace(go.Scatter(
                    x=scale_values, y=ref_flat, mode="lines",
                    name="O(n) reference",
                    line=dict(color="#6C63FF", width=1.5, dash="dot"),
                    showlegend=False,
                ))
                # Annotation: O(sqrt(n)) reference slope
                ref_ivf = ivf_avgs[0] * np.sqrt(np.array(scale_values) / scale_values[0])
                fig_scaling.add_trace(go.Scatter(
                    x=scale_values, y=ref_ivf, mode="lines",
                    name="O(√n) reference",
                    line=dict(color="#F59E0B", width=1.5, dash="dot"),
                    showlegend=False,
                ))

                fig_scaling.update_layout(
                    height=450,
                    xaxis=dict(
                        title="Catalog size (vectors)", type="log",
                        tickvals=scale_values, ticktext=scales_labels,
                    ),
                    yaxis=dict(
                        title="Avg search time (ms)", type="log",
                        exponentformat="SI",
                    ),
                    hovermode="x unified",
                    margin=dict(l=20, r=20, t=10, b=20),
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=theme["text"], size=12),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                st.plotly_chart(fig_scaling, use_container_width=True)

                # ---- Scaling ratio analysis ----
                st.markdown("### Real vs Theoretical Scaling")
                flat_ratio_actual = flat_avgs[2] / flat_avgs[0]
                ivf_ratio_actual = ivf_avgs[2] / ivf_avgs[0]
                import math
                flat_ratio_theory = 100  # O(n) from 1K to 100K
                ivf_ratio_theory = math.sqrt(100)  # O(sqrt(n)) = 10x

                analysis_cols = st.columns([1, 1])
                with analysis_cols[0]:
                    flat_pct = (flat_ratio_actual / flat_ratio_theory) * 100
                    st.markdown(
                        f"""
                        <div class="custom-card">
                            <h4 style="color:#6C63FF; margin-bottom:0.5rem;">FlatIP — O(n)</h4>
                            <table style="width:100%; font-size:0.9rem;">
                                <tr><td style="padding:0.3rem 0;">1K→100K ratio</td>
                                    <td style="text-align:right; font-weight:700;">{flat_ratio_actual:.1f}x</td></tr>
                                <tr><td style="padding:0.3rem 0;">Theoretical O(n)</td>
                                    <td style="text-align:right; font-weight:700;">{flat_ratio_theory:.0f}x</td></tr>
                                <tr><td style="padding:0.3rem 0;">Match</td>
                                    <td style="text-align:right; font-weight:700; color:#10B981;">{flat_pct:.0f}%</td></tr>
                            </table>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with analysis_cols[1]:
                    ivf_pct = (ivf_ratio_actual / ivf_ratio_theory) * 100
                    st.markdown(
                        f"""
                        <div class="custom-card">
                            <h4 style="color:#F59E0B; margin-bottom:0.5rem;">IVFFlat — O(√n)</h4>
                            <table style="width:100%; font-size:0.9rem;">
                                <tr><td style="padding:0.3rem 0;">1K→100K ratio</td>
                                    <td style="text-align:right; font-weight:700;">{ivf_ratio_actual:.1f}x</td></tr>
                                <tr><td style="padding:0.3rem 0;">Theoretical O(√n)</td>
                                    <td style="text-align:right; font-weight:700;">{ivf_ratio_theory:.1f}x</td></tr>
                                <tr><td style="padding:0.3rem 0;">Match</td>
                                    <td style="text-align:right; font-weight:700; color:#10B981;">{ivf_pct:.0f}%</td></tr>
                            </table>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.15); 
                                border-radius: 12px; padding: 1.2rem; margin-top:0.75rem;">
                        <p style="margin: 0; opacity: 0.85;">
                            <strong>🎯 Key insight:</strong> As the catalog grows from 
                            <strong>1K → 10K → 100K</strong> vectors, FlatIP search time 
                            scales <strong>{flat_ratio_actual:.0f}x</strong> (close to the theoretical 
                            O(n) = 100x), while IVFFlat scales only <strong>{ivf_ratio_actual:.1f}x</strong> 
                            (close to the theoretical O(√n) = 10.0x). 
                            At 100K vectors, IVFFlat is already <strong>{raw[100]['speedup']:.0f}x faster</strong> 
                            than brute-force — and the gap grows with every order of magnitude.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:
        # Show placeholder before running
        st.info(
            """
            👆 Click **"🚀 Run Benchmark"** to start a live comparison of FlatIP vs IVFFlat search performance.
            
            The benchmark will run multiple timed searches on the Siamese embedding dataset (1,199 vectors × 128 dims)
            and display interactive charts showing speed, accuracy, and projected performance at scale.
            """,
        )

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.markdown(
                """
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 1.5rem;">📊</div>
                    <h4>1,199 vectors</h4>
                    <p style="font-size: 0.85rem; opacity: 0.7;">Siamese embeddings (128-dim)</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                """
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 1.5rem;">⚡</div>
                    <h4>FlatIP vs IVFFlat</h4>
                    <p style="font-size: 0.85rem; opacity: 0.7;">Exact vs approximate search</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                """
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 1.5rem;">🎯</div>
                    <h4>Adjustable nprobe</h4>
                    <p style="font-size: 0.85rem; opacity: 0.7;">Speed vs accuracy trade-off</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
