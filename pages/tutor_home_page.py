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

# Set up page config
st.set_page_config(page_title="TutorConnect | Learn Better", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

# Custom styles using inline CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kumbh+Sans&display=swap');

    html, body, .stApp {
        font-family: 'Kumbh Sans', sans-serif;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    .navbar {
        background-color: #4B7BE5;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 8px;
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
        margin-top: 2rem;
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

    </style>
""", unsafe_allow_html=True)

# ----------------- Navbar ------------------
st.markdown("""
<div class="navbar">
    <div><strong>TutorConnect</strong></div>
    <div>
        <a href="#">About Us</a>
        <a href="#">Profile</a>
        <a href="#">Students</a>
        <a href="#">Subjects</a>
        <a href="#">Sign Out</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Hero Section ------------------
st.markdown("""
<div class="hero">
    <h1>Start Your Career Now</h1>
    <p>Personalized experience for every employee, anytime, anywhere.</p>
</div>
""", unsafe_allow_html=True)
