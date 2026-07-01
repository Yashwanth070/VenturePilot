import streamlit as st
import requests
import json
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.pdf_export import generate_startup_report
from frontend.components.layout import apply_layout

logged_in = apply_layout("Validation Engine")
if not logged_in:
    st.warning("Please log in from the main page.")
    st.stop()
st.markdown("Submit your startup idea for deep ML and AI analysis.")

# --- Sidebar AI Chatbot ---
st.sidebar.title("💬 AI Co-Founder")
st.sidebar.markdown("Ask follow-up questions about your startup.")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

for msg in st.session_state['chat_history']:
    with st.sidebar.chat_message(msg['role']):
        st.markdown(msg['content'])

with st.sidebar.form(key="chat_form", clear_on_submit=True):
    prompt = st.text_input("Ask a question...")
    submit_chat = st.form_submit_button("Send")

if submit_chat and prompt:
    with st.sidebar.chat_message("user"):
        st.markdown(prompt)
    st.session_state['chat_history'].append({"role": "user", "content": prompt})
    
    chat_payload = {
        "message": prompt,
        "history": st.session_state['chat_history'][:-1],
        "context": st.session_state.get('last_analysis', 'No analysis generated yet.')
    }
    with st.sidebar.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_res = requests.post("http://localhost:5001/api/chat", json=chat_payload)
                if chat_res.status_code == 200:
                    reply = chat_res.json().get('reply', 'Error')
                    st.markdown(reply)
                    st.session_state['chat_history'].append({"role": "assistant", "content": reply})
                else:
                    st.error("Failed to connect.")
            except:
                st.error("Backend error.")
# --------------------------

with st.form("startup_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Startup Name")
        industry = st.selectbox("Industry", ['AI', 'SaaS', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce', 'Web3', 'Cybersecurity'])
        problem = st.text_area("Problem Statement", height=100)
        team_size = st.number_input("Team Size", min_value=1, value=3)
        market_size = st.number_input("Market Size (Billions $)", min_value=0.1, value=1.0)
        
    with col2:
        solution = st.text_area("Solution Description", height=100)
        revenue_model = st.selectbox("Revenue Model", ['B2B Subscription', 'B2C Subscription', 'Freemium', 'Marketplace', 'One-time Sales', 'Ad-supported'])
        target_audience = st.text_input("Target Audience")
        competition = st.selectbox("Competition Level", ['Low', 'Medium', 'High'])
        innovation = st.slider("Innovation Score (Self-assessed)", 1, 10, 7)
        
    submit = st.form_submit_button("Analyze Startup", type="primary")

if submit:
    if not name or not problem or not solution:
        st.error("Please fill in all required text fields.")
    else:
        with st.spinner("🧠 AI is analyzing your startup..."):
            payload = {
                "user_id": st.session_state['user']['id'],
                "Industry": industry,
                "Team_Size": team_size,
                "Market_Size_B": market_size,
                "Revenue_Model": revenue_model,
                "Competition_Level": competition,
                "Innovation_Score": innovation,
                "details": f"Name: {name}\nIndustry: {industry}\nProblem: {problem}\nSolution: {solution}\nTarget: {target_audience}\nRevenue: {revenue_model}"
            }
            
            try:
                # Attempt to call backend API
                res = requests.post("http://localhost:5001/api/analyze/startup", json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    st.session_state['last_analysis'] = json.dumps(data) # For chatbot context
                    st.success("Analysis Complete!")
                    
                    # Display Scores
                    st.markdown("### 🎯 Prediction Engine")
                    score = data.get('prediction', {}).get('success_probability', 50)
                    method = data.get('prediction', {}).get('method', 'Unknown')
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        title = {'text': f"Success Probability (%)<br><span style='font-size:0.8em;color:gray'>Method: {method}</span>"},
                        gauge = {'axis': {'range': [None, 100]},
                                 'bar': {'color': "#58a6ff"},
                                 'steps' : [
                                     {'range': [0, 40], 'color': "rgba(248, 81, 73, 0.3)"},
                                     {'range': [40, 70], 'color': "rgba(227, 179, 65, 0.3)"},
                                     {'range': [70, 100], 'color': "rgba(63, 185, 80, 0.3)"}],
                                 'threshold' : {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': score}}))
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display Gemini Results in Tabs
                    st.markdown("### 🤖 Generative AI Insights")
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["SWOT Analysis", "Competitors", "Roadmap", "Business Model", "Pitch & Funding"])
                    
                    with tab1:
                        st.markdown(data.get('swot', 'No data'))
                    with tab2:
                        st.markdown(data.get('competitors', 'No data'))
                    with tab3:
                        st.markdown(data.get('roadmap', 'No data'))
                    with tab4:
                        st.markdown(data.get('bmc', 'No data'))
                    with tab5:
                        st.markdown("#### Investor Pitch")
                        st.markdown(data.get('pitch', 'No data'))
                        st.divider()
                        st.markdown("#### Funding Strategy")
                        st.markdown(data.get('funding', 'No data'))
                        
                    st.divider()
                    st.markdown("### 📥 Export Report")
                    pdf_buffer = generate_startup_report(data)
                    st.download_button(
                        label="Download Full PDF Report",
                        data=pdf_buffer,
                        file_name=f"{name.replace(' ', '_')}_Analysis.pdf",
                        mime="application/pdf"
                    )
                        
                else:
                    st.error(f"Backend Error: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to Backend: {e}")
                st.info("Make sure the Flask backend is running on port 5001.")
