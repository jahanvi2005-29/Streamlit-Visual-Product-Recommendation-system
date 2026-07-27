"""
Page 3 — Model Comparison
Interactive Plotly charts comparing Precision@5, Recall@5, and Multi-K results.
"""

import streamlit as st
import plotly.express as px
from utils.theme import get_theme
from utils.data_loader import load_final_comparison, load_multi_k_comparison, get_image_path


def show():
    theme = get_theme()

    st.markdown(
        """
        <h1>📊 Model Comparison</h1>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 700px;">
            Quantitative comparison of all three visual retrieval approaches on 
            Precision@5, Recall@5, and multi-K metrics.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Load data
    final_df = load_final_comparison()
    multi_k_df = load_multi_k_comparison()

    if final_df is None:
        st.error("Could not load comparison data from data/final_comparison.csv")
        return

    # ---- Headline visual ----
    img_path = get_image_path("final_comparison_bar_chart.png")
    if img_path:
        st.image(img_path, use_container_width=True)
        st.caption("Final comparison of Precision@5 across all three models")

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ---- Interactive Plotly charts ----
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Precision@5 Comparison")

        fig1 = px.bar(
            final_df,
            x="Model",
            y="Precision@5",
            color="Model",
            color_discrete_map={
                "Baseline (pretrained)": "#6B7280",
                "Transfer Learning": "#8B83FF",
                "Siamese Network": "#6C63FF",
            },
            text="Precision@5",
            labels={"Precision@5": "Precision@5", "Model": ""},
        )
        fig1.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig1.update_layout(
            height=350,
            showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
            yaxis_range=[0.95, 1.0],
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Recall@5 Comparison")

        fig2 = px.bar(
            final_df,
            x="Model",
            y="Recall@5",
            color="Model",
            color_discrete_map={
                "Baseline (pretrained)": "#6B7280",
                "Transfer Learning": "#8B83FF",
                "Siamese Network": "#6C63FF",
            },
            text="Recall@5",
            labels={"Recall@5": "Recall@5", "Model": ""},
        )
        fig2.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig2.update_layout(
            height=350,
            showlegend=False,
            margin=dict(l=20, r=20, t=10, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"], size=12),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---- Multi-K chart ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Performance Across K Values (5, 20, 50)")

    if multi_k_df is not None:
        col1, col2 = st.columns(2)

        with col1:
            fig3 = px.line(
                multi_k_df,
                x="K",
                y="Precision",
                color="Model",
                markers=True,
                color_discrete_map={
                    "Baseline": "#6B7280",
                    "Transfer Learning": "#8B83FF",
                    "Siamese": "#6C63FF",
                },
                labels={"Precision": "Precision", "K": "K"},
            )
            fig3.update_traces(line=dict(width=3), marker=dict(size=10))
            fig3.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=10, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=theme["text"], size=12),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            fig4 = px.line(
                multi_k_df,
                x="K",
                y="Recall",
                color="Model",
                markers=True,
                color_discrete_map={
                    "Baseline": "#6B7280",
                    "Transfer Learning": "#8B83FF",
                    "Siamese": "#6C63FF",
                },
                labels={"Recall": "Recall", "K": "K"},
            )
            fig4.update_traces(line=dict(width=3), marker=dict(size=10))
            fig4.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=10, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=theme["text"], size=12),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ---- Styled Data Table ----
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Detailed Comparison Table")

    # Format the data
    display_df = final_df.copy()
    display_df.columns = ["Model", "Precision@5", "Recall@5", "Embedding Time (s)"]

    # Build HTML table with conditional formatting
    best_precision = display_df["Precision@5"].max()
    best_recall = display_df["Recall@5"].max()
    best_time = display_df["Embedding Time (s)"].min()

    html_rows = ""
    for _, row in display_df.iterrows():
        is_best_p = row["Precision@5"] == best_precision
        is_best_r = row["Recall@5"] == best_recall
        is_best_t = row["Embedding Time (s)"] == best_time

        html_rows += f"""
        <tr>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {theme['border']}; font-weight: {600 if 'Siamese' in row['Model'] else 400};">
                {"🏆 " if 'Siamese' in row['Model'] else ""}{row['Model']}
            </td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {theme['border']}; text-align: center;
                       {f'background: rgba(16,185,129,0.15); color: #10B981; font-weight: 700;' if is_best_p else 'opacity: 0.8;'}">
                {row['Precision@5']:.3f}
            </td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {theme['border']}; text-align: center;
                       {f'background: rgba(16,185,129,0.15); color: #10B981; font-weight: 700;' if is_best_r else 'opacity: 0.8;'}">
                {row['Recall@5']:.4f}
            </td>
            <td style="padding: 0.75rem 1rem; border-top: 1px solid {theme['border']}; text-align: center;
                       {f'background: rgba(16,185,129,0.15); color: #10B981; font-weight: 700;' if is_best_t else 'opacity: 0.8;'}">
                {row['Embedding Time (s)']:.1f}s
            </td>
        </tr>
        """

    st.markdown(
        f"""
        <table style="width:100%; border-collapse: collapse; border-radius: 12px; overflow: hidden;">
            <thead>
                <tr style="background: rgba(108,99,255,0.1);">
                    <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600;">Model</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Precision@5</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Recall@5</th>
                    <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600;">Embedding Time</th>
                </tr>
            </thead>
            <tbody>
                {html_rows}
            </tbody>
        </table>
        <p style="text-align: right; font-size: 0.75rem; opacity: 0.5; margin-top: 0.3rem;">
            ✅ Green highlighted cells indicate the best score in each column
        </p>
        """,
        unsafe_allow_html=True,
    )
