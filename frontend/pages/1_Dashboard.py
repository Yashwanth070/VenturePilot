import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from frontend.components.layout import apply_layout

logged_in = apply_layout("Dashboard")
if not logged_in:
    st.warning("Please log in from the main page.")
    st.stop()

st.markdown("Overview of your startup analyses and platform metrics.")

# Mock data for demonstration of premium charts
np.random.seed(42)
df_trends = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=30),
    'Analyses': np.random.randint(5, 25, 30),
    'Avg_Success_Score': np.random.uniform(40, 85, 30)
})

# ProjectHub Style Metrics Grid
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;">
    <div class="ph-stat-card">
        <div class="ph-stat-icon gold">📁</div>
        <div class="ph-stat-content">
            <div class="ph-stat-value">124</div>
            <div class="ph-stat-label">Total Analyses</div>
        </div>
    </div>
    <div class="ph-stat-card">
        <div class="ph-stat-icon blue">📋</div>
        <div class="ph-stat-content">
            <div class="ph-stat-value">76/100</div>
            <div class="ph-stat-label">Avg Success Score</div>
        </div>
    </div>
    <div class="ph-stat-card">
        <div class="ph-stat-icon green">✅</div>
        <div class="ph-stat-content">
            <div class="ph-stat-value">68/100</div>
            <div class="ph-stat-label">Investor Readiness</div>
        </div>
    </div>
    <div class="ph-stat-card">
        <div class="ph-stat-icon purple">⭐</div>
        <div class="ph-stat-content">
            <div class="ph-stat-value">AI</div>
            <div class="ph-stat-label">Top Industry</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Activity Trends")
fig = px.line(df_trends, x='Date', y='Analyses', title="Startup Analyses Over Time", 
              template="plotly_dark", line_shape='spline')
fig.update_traces(line_color='#58a6ff', line_width=3)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Industry Distribution")
    industries = pd.DataFrame({
        'Industry': ['AI', 'SaaS', 'Fintech', 'Healthtech', 'Web3'],
        'Count': [45, 30, 20, 15, 14]
    })
    fig_pie = px.pie(industries, values='Count', names='Industry', hole=0.6, template="plotly_dark",
                     color_discrete_sequence=['#58a6ff', '#a371f7', '#3fb950', '#f85149', '#e3b341'])
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("### Risk vs Innovation Matrix")
    scatter_df = pd.DataFrame({
        'Innovation Score': np.random.uniform(1, 10, 50),
        'Risk Level': np.random.uniform(1, 10, 50),
        'Industry': np.random.choice(['AI', 'SaaS', 'Fintech'], 50)
    })
    fig_scatter = px.scatter(scatter_df, x='Innovation Score', y='Risk Level', color='Industry', 
                             template="plotly_dark", size_max=10,
                             color_discrete_sequence=['#58a6ff', '#a371f7', '#3fb950'])
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
