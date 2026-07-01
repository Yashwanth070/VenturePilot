import streamlit as st
import os

def apply_layout(page_title):
    st.set_page_config(
        page_title=f"VenturePilot | {page_title}",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    # Inject Theme Variables
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    :root, .stApp {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --text-primary: #ffffff;
        --text-secondary: #999999;
        --card-bg: #050505;
        --card-border: rgba(255, 255, 255, 0.1);
        --card-hover: rgba(255, 255, 255, 0.2);
        --input-bg: #0a0a0a;
        --btn-primary: #ffffff;
        --btn-primary-text: #000000;
        --accent-glow: transparent;
    }
    </style>
    """ if st.session_state['theme'] == 'dark' else """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    :root, .stApp {
        --bg-primary: #ffffff;
        --bg-secondary: #f7f7f7;
        --text-primary: #000000;
        --text-secondary: #5e5e5e;
        --card-bg: #ffffff;
        --card-border: rgba(0, 0, 0, 0.08);
        --card-hover: rgba(0, 0, 0, 0.15);
        --input-bg: #ffffff;
        --btn-primary: #000000;
        --btn-primary-text: #ffffff;
        --accent-glow: transparent;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    # Inject Custom CSS
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/custom.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    if st.session_state['user'] is None:
        st.markdown("""
            <style>
                [data-testid="collapsedControl"] { display: none !important; }
                section[data-testid="stSidebar"] { display: none !important; }
            </style>
        """, unsafe_allow_html=True)
        t_col1, t_col2 = st.columns([10, 1.5])
        with t_col2:
            theme_icon = "☀️ Light" if st.session_state['theme'] == 'dark' else "🌙 Dark"
            if st.button(theme_icon, use_container_width=True, key="theme_toggle_out"):
                st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
                st.rerun()
        return False

    # We will rely on Streamlit's native multipage router (stSidebarNav) 
    # to handle navigation without doing a full page reload.
    # The native nav is styled in custom.css to look like ProjectHub.
    
    # Bottom User Profile (Streamlit places user markdown below the native nav)
    st.sidebar.markdown("<div style='margin-top: 48px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 4px;'>
            <div style='width: 32px; height: 32px; background: var(--text-primary); color: var(--bg-primary); display: flex; align-items: center; justify-content: center; border-radius: 4px; font-weight: 600; font-size: 14px;'>
                {st.session_state['user']['name'][0]}
            </div>
            <div>
                <div style='font-size: 14px; font-weight: 500; color: var(--text-primary); line-height: 1.2;'>{st.session_state['user']['name']}</div>
                <div style='font-size: 12px; color: var(--text-secondary); line-height: 1.2; margin-top: 2px;'>Founder</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("Sign Out", use_container_width=True, type="secondary"):
        st.session_state['user'] = None
        st.rerun()

    # Top Navbar
    nav_left, nav_right = st.columns([8, 2])
    with nav_left:
        st.markdown(f"<h2 style='margin-bottom: 0; padding-bottom: 0; border: none; font-size: 20px; font-weight: 600;'>{page_title}</h2>", unsafe_allow_html=True)
    with nav_right:
        theme_icon = "☀️" if st.session_state['theme'] == 'dark' else "🌙"
        if st.button(f"{theme_icon} Toggle Theme", key="theme_toggle_in", use_container_width=True, type="secondary"):
            st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
            st.rerun()
            
    st.markdown("<hr style='margin-top: 12px; margin-bottom: 32px; border: none; border-top: 1px solid var(--card-border);'>", unsafe_allow_html=True)

    return True
