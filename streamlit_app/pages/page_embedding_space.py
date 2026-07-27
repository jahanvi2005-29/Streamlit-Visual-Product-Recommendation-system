"""
Page 6 — Embedding Space Visualization (t-SNE)
t-SNE plots, before/after comparison, and training history curves.
"""

import streamlit as st
import plotly.express as px
from utils.theme import get_theme
from utils.data_loader import get_image_path, load_training_history


def show():
    theme = get_theme()

    st.markdown(
        """
        <h1>🔬 Embedding Space Visualization</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            t-SNE projections reveal how the Siamese Network restructures the embedding 
            space to create tight, well-separated clusters by product category.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- t-SNE: Siamese only ----
    st.markdown("### t-SNE: Siamese Network Embedding Space")

    img_path = get_image_path("tsne_siamese_only.png")
    if img_path:
        st.image(img_path, use_container_width=True)
    else:
        st.info("t-SNE image not found.")

    st.markdown(
        """
        <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.15); 
                    border-radius: 12px; padding: 1.2rem; margin-bottom: 2rem;">
            <p style="margin: 0; opacity: 0.85;">
                <strong>What to look for:</strong> Each color represents a different product category.
                Well-separated clusters mean the model has learned an embedding space where 
                visually similar items are close together — a key requirement for accurate 
                retrieval. Overlapping clusters would indicate the model confuses categories.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Before/After comparison ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Before vs After: Baseline → Siamese")

    img_path2 = get_image_path("tsne_before_after_baseline_vs_siamese.png")
    if img_path2:
        st.image(img_path2, use_container_width=True)
    else:
        st.info("Before/after t-SNE image not found.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center;">
                <h3>⬅️ Before (Baseline)</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    Generic ImageNet features produce a messy embedding space with significant 
                    category overlap. Items from different categories are scattered throughout, 
                    making it hard to retrieve visually consistent results.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center; border-color: #6C63FF; 
                        background: rgba(108,99,255,0.05);">
                <h3>➡️ After (Siamese) ✅</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    The Siamese embedding space shows tight, clearly separated clusters for 
                    each category. Items that look alike naturally group together — this is 
                    exactly what makes the Siamese Network's retrieval so accurate (99.7% Precision@5).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- Training Curves ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Training History")

    df = load_training_history()
    if df is not None:
        tab1, tab2 = st.tabs(["📈 Transfer Learning", "📉 Siamese Network (Triplet Loss)"])

        with tab1:
            tl_df = df[df["Model"] == "Transfer Learning"].copy()
            # Split into accuracy and loss
            tl_acc = tl_df[tl_df["Metric"].str.contains("accuracy", case=False)]
            tl_loss = tl_df[tl_df["Metric"].str.contains("loss", case=False)]

            col1, col2 = st.columns(2)
            with col1:
                fig_acc = px.line(
                    tl_acc, x="Epoch", y="Value", color="Metric",
                    markers=True, title="Accuracy",
                    color_discrete_map={
                        "train_accuracy": "#6C63FF",
                        "val_accuracy": "#10B981",
                    },
                )
                fig_acc.update_traces(line=dict(width=3), marker=dict(size=8))
                fig_acc.update_layout(
                    height=350,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=theme["text"], size=12),
                    legend=dict(orientation="h", y=-0.2),
                )
                st.plotly_chart(fig_acc, use_container_width=True)

            with col2:
                fig_loss = px.line(
                    tl_loss, x="Epoch", y="Value", color="Metric",
                    markers=True, title="Loss",
                    color_discrete_map={
                        "train_loss": "#EF4444",
                        "val_loss": "#F59E0B",
                    },
                )
                fig_loss.update_traces(line=dict(width=3), marker=dict(size=8))
                fig_loss.update_layout(
                    height=350,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=theme["text"], size=12),
                    legend=dict(orientation="h", y=-0.2),
                )
                st.plotly_chart(fig_loss, use_container_width=True)

        with tab2:
            siamese_df = df[df["Model"] == "Siamese Network"].copy()

            if not siamese_df.empty:
                fig_triplet = px.line(
                    siamese_df, x="Epoch", y="Value", color="Metric",
                    markers=True,
                    color_discrete_map={"triplet_loss": "#6C63FF"},
                )
                fig_triplet.update_traces(line=dict(width=3, color="#6C63FF"), marker=dict(size=10, color="#6C63FF"))
                fig_triplet.update_layout(
                    height=400,
                    title="Triplet Loss over Training Epochs",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=theme["text"], size=12),
                )
                # Add annotations
                min_loss = siamese_df["Value"].min()
                min_epoch = siamese_df[siamese_df["Value"] == min_loss]["Epoch"].values[0]
                fig_triplet.add_annotation(
                    x=min_epoch,
                    y=min_loss,
                    text=f"Epoch {min_epoch}: {min_loss:.4f}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowcolor="#6C63FF",
                    font=dict(size=11, color="#6C63FF"),
                )
                st.plotly_chart(fig_triplet, use_container_width=True)

                st.markdown(
                    """
                    <div style="background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); 
                                border-radius: 12px; padding: 1.2rem;">
                        <p style="margin: 0; opacity: 0.85;">
                            📉 <strong>Triplet loss dropped from 5.24 → 0.45</strong> in just 3 epochs,
                            demonstrating fast convergence. The Siamese Network rapidly learns
                            to organize the embedding space so that anchor-positive pairs are close
                            and anchor-negative pairs are far apart.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Siamese Network training data not available.")
    else:
        st.info("Training history CSV not found in data/ folder.")
