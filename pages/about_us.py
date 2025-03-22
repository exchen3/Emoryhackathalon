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

load_dotenv()

# Page setup
st.set_page_config(page_title="About Us | TutorConnect", layout="wide")

# Page styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');

    html, body, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: url('https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
        color: #333;
    }

    .overlay {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        margin: 2rem auto;
        max-width: 1200px;
    }

    .highlight {
        color: #FF2400;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }

    .team-img {
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .team-card {
        text-align: center;
        padding: 2rem 1rem;
        border-radius: 12px;
        background: white;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .team-card:hover {
        transform: translateY(-5px);
    }

    .team-card img {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        margin-bottom: 1rem;
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

# Overlay content
st.markdown('<div class="overlay">', unsafe_allow_html=True)

st.markdown("""
<div class="text-center mb-5">
    <h1 class="display-4 fw-bold">About <span class="highlight">TutorConnect</span></h1>
    <p class="lead">Empowering education by connecting underrepresented students with qualified, passionate tutors.</p>
</div>
""", unsafe_allow_html=True)

# Mission Section
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1584697964192-886b60f6c865?auto=format&fit=crop&w=1350&q=80", use_column_width=True)
with col2:
    st.markdown('<h2 class="section-title">Our Mission</h2>', unsafe_allow_html=True)
    st.write("At TutorConnect, we believe every student deserves access to quality, personalized education. "
             "Our platform bridges the connection between eager learners and experienced tutors, providing flexible "
             "and effective academic support anywhere, anytime.")

st.markdown("<br>", unsafe_allow_html=True)

# Team Section
col3, col4 = st.columns(2)
with col4:
    st.image("https://images.unsplash.com/photo-1581090700227-1f94d44aa8bf?auto=format&fit=crop&w=1350&q=80", use_column_width=True)
with col3:
    st.markdown('<h2 class="section-title">Meet the Team</h2>', unsafe_allow_html=True)
    st.write("We're a diverse group of students at Emory University passionate about redefining the future of student learning.")

st.markdown("### ", unsafe_allow_html=True)

# Team Members
cols = st.columns(4)
team = [
    {"name": "Eric Chen", "role": "Co-Founder & CEO", "img": "https://randomuser.me/api/portraits/women/68.jpg"},
    {"name": "Andy Dang", "role": "CTO & Lead Developer", "img": "https://randomuser.me/api/portraits/men/43.jpg"},
    {"name": "Lisa", "role": "Community Manager", "img": "https://randomuser.me/api/portraits/women/65.jpg"},
    {"name": "Lynne Zheng", "role": "Outreach Coordinator", "img": "https://randomuser.me/api/portraits/women/65.jpg"},
]

for col, member in zip(cols, team):
    with col:
        st.markdown(f"""
            <div class="team-card">
                <img src="{member['img']}" alt="{member['name']}"/>
                <h5 class="fw-bold">{member['name']}</h5>
                <p class="text-muted">{member['role']}</p>
            </div>
        """, unsafe_allow_html=True)

# Back to home
st.markdown("""
<div class="text-center mt-5">
    <a href="#" class="btn btn-primary btn-lg">Back to Home</a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close overlay
