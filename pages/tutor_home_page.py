import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

# Set up page config
st.set_page_config(page_title="TutorConnect | Learn Better", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] != "Tutor":
    st.warning("This page can only be accessed by tutors.")
    st.stop()


# Custom styles using inline CSS
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
        color: #4B7BE5;
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
    col_links = st.columns(6)

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
        if st.button("📌 Request List", use_container_width=True):
            st.switch_page("pages/tutor_request_list.py")

    with col_links[4]:
        if st.button("✅ Request Completion", use_container_width=True):
            st.switch_page("pages/tutor_completeness_status.py")

    with col_links[5]:
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

# ---- Hero Section ----
st.markdown("""
<div class="hero">
    <h1>Start Your Career Now</h1>
    <p>Personalized Experience for Every Tutor. Anytime, Anywhere.</p>
</div>
""", unsafe_allow_html=True)

# # ---- Services Section ----
# st.markdown("<div class='services'><h2 class='section_title'>Our Tutoring Services</h2></div>", unsafe_allow_html=True)

# # ---- Cards ----
# col1, = st.columns(1)

# with col1:
#     st.image("https://www.the74million.org/wp-content/uploads/2024/01/tutor-one-on-one.jpg", use_column_width=True)
#     st.subheader("Start Your Career Now")
#     st.write("Personalized experience for every employee, anytime, anywhere.")

# center_col1, center_col2, center_col3 = st.columns([1, 2, 1])

# with center_col2:
#     if st.button("FIND A TUTOR", use_container_width=True):
#         st.switch_page("pages/find_tutor.py")