import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import subprocess
import base64
import time

# Page config
st.set_page_config(page_title="TutorConnect | Learn Better", layout="wide")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    st.stop()

# Custom CSS (basic styles mimicking your HTML)
st.markdown("""
    <style>
    html, body {
        font-family: 'Kumbh Sans', sans-serif;
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
        background: linear-gradient(to right, #4B7BE5, #6FB1FC);
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
st.markdown('<div class="navbar-title">TutorConnect</div>', unsafe_allow_html=True)

# Use Streamlit's built-in page links for navigation
with st.container():
    col_links = st.columns(4)

    with col_links[0]:
        if st.button("🧭 About Us", use_container_width=True):
            st.switch_page("pages/about_us.py")

    with col_links[1]:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/student_profile.py")

    with col_links[2]:
        if st.button("🎓 Tutors", use_container_width=True):
            st.switch_page("pages/find_tutor.py")

    with col_links[3]:
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

st.markdown('</div>', unsafe_allow_html=True)

# ---- Hero Section ----
st.markdown("""
<div class="hero">
    <h1>Unlock Your Full Potential</h1>
    <p>Personalized tutoring for every learner, anytime, anywhere.</p>
    <a href="#" class="hero_cta">Find a Tutor</a>
</div>
""", unsafe_allow_html=True)

# ---- Services Section ----
st.markdown("<div class='services'><h2 class='section_title'>Our Tutoring Services</h2></div>", unsafe_allow_html=True)

# ---- Cards ----
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://www.the74million.org/wp-content/uploads/2024/01/tutor-one-on-one.jpg", use_column_width=True)
    st.subheader("One-on-One Tutoring")
    st.write("Work directly with a professional tutor who tailors lessons to your individual needs and pace.")

with col2:
    st.image("https://images.unsplash.com/photo-1522075469751-3a6694fb2f61", use_column_width=True)
    st.subheader("Group Sessions")
    st.write("Join small interactive study groups to learn collaboratively and stay motivated with peers.")

with col3:
    st.image("https://images.unsplash.com/photo-1607746882042-944635dfe10e", use_column_width=True)
    st.subheader("Online Resources")
    st.write("Access a wide library of lessons, quizzes, and study guides to support your learning journey anytime.")