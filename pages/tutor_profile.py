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

# Set page config
st.set_page_config(page_title="Tutor Profile", layout="centered")

# Sample tutor data (replace with your DB query)
tutor = {
    "name": "Jane Smith",
    "university": "Georgia Tech",
    "graduation_year": 2024,
    "major": "Computer Science",
    "employed_status": "Yes",
    "classes_teaching": "Data Structures, Algorithms, Machine Learning",
    "grad_school": "No",
    "email": "janesmith@example.com",
    "bio": "I love helping students understand complex CS topics in simple ways!"
}

# Custom CSS for background, navbar, and card layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');

    html, body, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
    }

    .navbar {
        background-color: #0d6efd;
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    .navbar a {
        color: white;
        margin-left: 1.5rem;
        text-decoration: none;
        font-weight: bold;
    }

    .profile-container {
        max-width: 720px;
        margin: 40px auto;
        background: rgba(255, 255, 255, 0.75);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }

    .profile-header {
        text-align: center;
        font-size: 2.2rem;
        color: #0d6efd;
        margin-bottom: 2rem;
    }

    .profile-field {
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }

    .profile-field strong {
        color: #333;
    }

    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <div><strong>TutorConnect</strong></div>
    <div>
        <a href="#">About Us</a>
        <a href="#">Profile</a>
        <a href="#">Tutors</a>
        <a href="#">Subjects</a>
        <a href="#">Sign Out</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Profile Card
st.markdown('<div class="profile-container">', unsafe_allow_html=True)
st.markdown('<div class="profile-header">Tutor Profile</div>', unsafe_allow_html=True)

# Render each profile field
def render_field(label, value):
    st.markdown(f'<div class="profile-field"><strong>{label}:</strong> {value}</div>', unsafe_allow_html=True)

render_field("Name", tutor["name"])
render_field("University", tutor["university"])
render_field("Graduation Year", tutor["graduation_year"])
render_field("Major", tutor["major"])
render_field("Employment Status", tutor["employed_status"])
render_field("Classes Teaching", tutor["classes_teaching"])
render_field("Grad School", tutor["grad_school"])
render_field("Email", tutor["email"])
render_field("Bio", tutor["bio"])

st.markdown('</div>', unsafe_allow_html=True)  # Close container