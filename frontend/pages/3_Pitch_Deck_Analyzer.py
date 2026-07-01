import streamlit as st
import requests
import plotly.express as px
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from frontend.components.layout import apply_layout

logged_in = apply_layout("Pitch Deck Analyzer")
if not logged_in:
    st.warning("Please log in from the main page.")
    st.stop()

st.title("📄 Pitch Deck Analyzer (Computer Vision)")
st.markdown("Upload your Pitch Deck (PDF) for layout, visual balance, and text density analysis via OpenCV.")

uploaded_file = st.file_uploader("Upload Pitch Deck (PDF format)", type=['pdf'])

if uploaded_file is not None:
    if st.button("Analyze Pitch Deck", type="primary"):
        with st.spinner("👁️ OpenCV is scanning your slides..."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
                data = {'user_id': st.session_state['user']['id']}
                
                res = requests.post("http://localhost:5001/api/analyze/pitchdeck", files=files, data=data)
                
                if res.status_code == 200:
                    results = res.json()
                    if "error" in results:
                        st.error(results["error"])
                    else:
                        st.success("Analysis Complete!")
                        
                        scores = results.get('scores', {})
                        metrics = results.get('metrics', {})
                        
                        st.markdown("### 🏆 Core Scores")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Overall Quality Score", f"{scores.get('quality_score')}/100")
                        c2.metric("Visual Design Score", f"{scores.get('visual_design_score')}/100")
                        c3.metric("Investor Readiness", f"{scores.get('investor_readiness_score')}/100")
                        
                        st.markdown("### 📊 Slide Metrics")
                        st.write(f"**Total Pages Analyzed:** {results.get('total_pages')}")
                        
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Avg Text Density", f"{metrics.get('average_text_density')}%")
                        c2.metric("Clutter Index", f"{metrics.get('average_clutter_index')}%")
                        c3.metric("Visual Balance", f"{metrics.get('visual_balance')}")
                        c4.metric("Visuals Ratio", f"{metrics.get('visuals_ratio')}")
                        
                        st.markdown("### 💡 Recommendations")
                        for rec in results.get('recommendations', []):
                            st.info(f"👉 {rec}")
                            
                        # Show slide by slide breakdown
                        st.markdown("### 📄 Slide-by-Slide Breakdown")
                        pages = results.get('pages', [])
                        if pages:
                            import pandas as pd
                            df_pages = pd.DataFrame(pages)
                            fig = px.bar(df_pages, x='page', y='text_density', title="Text Density per Slide (%)", template="plotly_dark")
                            fig.update_traces(marker_color='#a371f7')
                            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.dataframe(df_pages.style.background_gradient(cmap='Blues'), use_container_width=True)
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                st.info("Make sure the Flask backend is running and `pdf2image` & poppler are installed.")
