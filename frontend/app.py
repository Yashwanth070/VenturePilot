import streamlit as st
import os
import sys

# Ensure we can import the component
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from frontend.components.layout import apply_layout

logged_in = apply_layout("Home")

if not logged_in:
    # Centered Minimalist ProjectHub-Style Login UI
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1, 1.2]) # Narrower center column
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 32px;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--text-primary)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 24px;">
              <path d="M12 3v4"></path>
              <path d="M12 7l-4 14"></path>
              <path d="M12 7l4 14"></path>
              <path d="M9 13h6"></path>
              <path d="M12 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"></path>
            </svg>
            <h1 style="font-size: 28px; font-weight: 600; margin-bottom: 8px; color: var(--text-primary); background: none; -webkit-text-fill-color: var(--text-primary); letter-spacing: -0.5px;">Welcome Back</h1>
            <p style="color: var(--text-secondary); font-size: 15px;">Enter your credentials to access your workspace.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size: 11px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; letter-spacing: 1px;'>EMAIL ADDRESS</div>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="name@company.com", label_visibility="collapsed")
        
        st.markdown("""
        <div style='display: flex; justify-content: space-between; font-size: 11px; font-weight: 600; color: var(--text-secondary); margin-top: 24px; margin-bottom: 8px; letter-spacing: 1px;'>
            <span>PASSWORD</span>
            <span style='cursor: pointer; font-weight: 500; color: var(--text-primary); letter-spacing: normal;'>Forgot?</span>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("Password", placeholder="••••••••", type="password", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True, type="primary"):
            st.session_state['user'] = {"id": "1", "email": email, "name": "Founder"}
            st.rerun()
            
        # Divider
        st.markdown("""
            <div style="display: flex; align-items: center; text-align: center; margin: 32px 0; color: var(--text-secondary); font-size: 13px;">
                <div style="flex: 1; border-bottom: 1px solid var(--card-border); margin-right: 1.5em;"></div>
                or continue with
                <div style="flex: 1; border-bottom: 1px solid var(--card-border); margin-left: 1.5em;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # OAuth Grid
        scol1, scol2 = st.columns(2)
        with scol1:
            if st.button("Google", use_container_width=True):
                st.session_state['user'] = {"id": "1", "email": "google@example.com", "name": "Google User"}
                st.rerun()
        with scol2:
            if st.button("GitHub", use_container_width=True):
                st.session_state['user'] = {"id": "1", "email": "github@example.com", "name": "GitHub User"}
                st.rerun()
                
        st.markdown("<div style='text-align: center; font-size: 14px; margin-top: 32px; color: var(--text-secondary);'>Don't have an account? <span style='color: var(--text-primary); font-weight: 500; cursor: pointer;'>Get started</span></div>", unsafe_allow_html=True)

else:
    st.markdown("### 👋 Welcome to VenturePilot")
    st.markdown("You are successfully logged in. Please select a module from the **Sidebar Menu** to begin your startup analysis.")
