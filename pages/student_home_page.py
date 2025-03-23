import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

# Page config
st.set_page_config(page_title="Student Home Page", layout="wide")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] != "Student":
    st.warning("This page can only be accessed by students.")
    st.stop()

# Custom CSS (basic styles mimicking your HTML)
st.markdown("""
    <style>
    html, body {
        font-family: 'Kumbh Sans', sans-serif;
    }
    
    .center-btn {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
    }
    
    .navbar {
        background-color: #4B7BE5;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        margin-left: 1.5rem;
        font-weight: bold;
    }
    .hero {
        background: linear-gradient(to right, #800020, #E0115F);
        color: white;
        padding: 4rem 2rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero p {
        font-size: 1.25rem;
    }
    .hero_cta {
        background-color: white;
        color: #4B7BE5;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-decoration: none;
        margin-top: 1.5rem;
        display: inline-block;
    }
    .services h2 {
        text-align: center;
        margin-bottom: 2rem;
        font-size: 2rem;
        color: #ffffff;
    }
    .card img {
        border-radius: 10px;
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

def logout():
    # Clear session state
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("You have been logged out.")
    time.sleep(1)
    st.switch_page("login.py")  # Navigate to login page

# ---- Navbar ----
st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
# st.markdown('<div class="navbar-title">TutorConnect</div>', unsafe_allow_html=True)

# Use Streamlit's built-in page links for navigation
with st.container():
    col_links = st.columns(7)

    with col_links[0]:
        if st.button("🏠 Home", use_container_width=True):
            role = st.session_state.get("role")
            if role == "Student":
                st.switch_page("pages/student_home_page.py")
            elif role == "Tutor":
                st.switch_page("pages/tutor_home_page.py")

    with col_links[1]:
        if st.button("🧭 About Us", use_container_width=True):
            st.switch_page("pages/about_us.py")

    with col_links[2]:
        if st.button("👤 Profile", use_container_width=True):
            if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
                st.warning("Please log in first!")
                time.sleep(1)
                st.switch_page("login.py")
            else:
                role = st.session_state.get("role")
                if role == "Student":
                    st.switch_page("pages/student_profile.py")
                elif role == "Tutor":
                    st.switch_page("pages/tutor_profile.py")

    with col_links[3]:
        if st.button("🎓 Tutors", use_container_width=True):
            st.switch_page("pages/find_tutor.py")

    with col_links[4]:
        if st.button("📌 Request List", use_container_width=True):
            st.switch_page("pages/student_request_record.py")

    with col_links[5]:
        if st.button("✅ Request Completion", use_container_width=True):
            st.switch_page("pages/student_completeness_status.py")

    with col_links[6]:
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

st.markdown('</div>', unsafe_allow_html=True)

# ---- Hero Section ----
st.markdown("""
<div class="hero">
    <h1>Unlock Your Full Potential</h1>
    <p>Personalized tutoring for every learner. Anytime, anywhere.</p>
</div>
""", unsafe_allow_html=True)

center_col1, center_col2, center_col3 = st.columns([1, 2, 1])

with center_col2:
    if st.button("FIND A TUTOR", use_container_width=True):
        st.switch_page("pages/find_tutor.py")