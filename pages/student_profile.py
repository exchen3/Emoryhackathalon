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

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")

schema_name = "emoryhackathon"
print("DEBUG ENV:")
print("DB_USERNAME =", os.getenv("DB_USERNAME"))
print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))
print("DB_HOST =", os.getenv("DB_HOST"))
# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")

schema_name = "emoryhackathon"

# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")
username = st.session_state["username"]

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")

schema_name = "emoryhackathon"

# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")
username = st.session_state["username"]

# Page configuration
st.set_page_config(page_title="Student Profile", layout="centered")
<<<<<<< Updated upstream
username = st.session_state["username"]
retrieve_query = text(f"SELECT * FROM student WHERE user_id = '{username}'")
with engine.connect() as conn:
    result = conn.execute(retrieve_query).fetchone()
=======

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    st.stop()

try:
    with engine.connect() as conn:
        query = text(f"SELECT * FROM student WHERE user_id = :username")
        result = conn.execute(query, {"username": username}).fetchone()

        if result and result[0] == hashed_password:
            st.success(f"Welcome, {username}!")

            # Store user login state
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role

            # Redirect to according info page
            if role == "Student":
                st.switch_page("pages/student_info_input.py")
            elif role == "Tutor":
                st.switch_page("pages/tutor_info_input.py")
        else:
            st.error("Invalid username or password.")
except Exception as e:
    st.error(f"Database error: {e}")  

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
# TODO: Replace the student with real data retrieval from database
student = {
    "name": result[2],
    "university": result[3],
    "graduation_year": result[4],
    "major": result[5],
    "gpa_range": result[9],
    "classes_taking": result[10],
    "bio": result[11],
    "email": result[12]
}

# Inject CSS for background and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');

    html, body, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
    }

    .navbar {
        background-color: #0d6efd;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .navbar a {
        color: white;
        text-decoration: none;
        margin-left: 1.5rem;
        font-weight: bold;
    }

    .profile-container {
        max-width: 720px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.75);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }

    .profile-header {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: #0d6efd;
    }

    .profile-field {
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }

    .edit-btn {
        display: block;
        margin: 2rem auto 0;
        text-align: center;
        background: #0d6efd;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <div class="navbar_logo"><strong>TutorConnect</strong></div>
    <div class="navbar_menu">
        <a href="#">About Us</a>
        <a href="#">Profile</a>
        <a href="#">Tutors</a>
        <a href="#">Subjects</a>
        <a href="#">Sign Out</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Profile content
st.markdown('<div class="profile-container">', unsafe_allow_html=True)
st.markdown('<h1 class="profile-header">Student Profile</h1>', unsafe_allow_html=True)

def render_field(label, value):
    st.markdown(f'<div class="profile-field"><strong>{label}:</strong> {value}</div>', unsafe_allow_html=True)

render_field("Name", student["name"])
render_field("University", student["university"])
render_field("Graduation Year", student["graduation_year"])
render_field("Major", student["major"])
render_field("GPA Range", student["gpa_range"])
render_field("Classes Taking", student["classes_taking"])
render_field("Bio", student["bio"])
render_field("Email", student["email"])

# Edit Profile Button
st.markdown('<a class="edit-btn" href="#">Edit Profile</a>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End of profile-container