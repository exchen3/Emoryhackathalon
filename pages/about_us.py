import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()

# Page setup
st.set_page_config(page_title="About Us", layout="wide")

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
    col_links = st.columns(5)

    with col_links[0]:
        if st.button("🏠 Home", use_container_width=True):
            role = st.session_state.get("role")
            if role == "Student":
                st.switch_page("pages/student_home_page.py")
            elif role == "Tutor":
                st.switch_page("pages/tutor_home_page.py")
            else:
                st.warning("Please log in first!")
                time.sleep(1)
                st.switch_page("login.py")

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
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

# Page styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');

    .centered-container {
    text-align: center;
    margin: 0 auto;
    max-width: 900px;
    padding: 2rem 1rem;
    }

    html, body, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-size: cover;
        color: #ffffff;
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center; /* This centers content vertically */
    text-align: center;
    padding: 2rem 1rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    color: black;
    height: 100%; /* Ensures uniform height if needed */
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

st.markdown("""
<div class="centered-container">
    <h1 class="display-4 fw-bold">About <span class="highlight">TutorConnect</span></h1>
    <p class="lead">Empowering education by connecting underrepresented students with qualified, passionate tutors.</p>
</div>
""", unsafe_allow_html=True)

# Mission Section
col1, col2 = st.columns(2)
with col1:
    st.image("https://www.spelman.edu/_2-Images/academics/french/french-tutor-2.jpg", use_column_width=True)
with col2:
    st.markdown('<h2 class="section-title">Our Mission</h2>', unsafe_allow_html=True)
    st.write("At TutorConnect, we believe every student deserves access to quality, personalized education. "
             "Our platform bridges the connection between eager learners and experienced tutors, providing flexible "
             "and effective academic support anywhere, anytime.")

st.markdown("<br>", unsafe_allow_html=True)

# Team Section
col3, col4 = st.columns(2)
with col4:
    st.image("https://test-bright.com/main/wp-content/uploads/2015/09/group-tutoring-large.jpg", use_column_width=True)
with col3:
    st.markdown('<h2 class="section-title">Meet the Team</h2>', unsafe_allow_html=True)
    st.write("We're a group of students at Emory University passionate about redefining the future of student learning.")

st.markdown("### ", unsafe_allow_html=True)

# Team Members
cols = st.columns(4)
team = [
    {"name": "Eric Chen", "role": "Developer", "img": "https://imgur.com/pZzky89.jpg"},
    {"name": "Andy Dang", "role": "Developer", "img": "https://imgur.com/YkAhX3k.jpg"},
    {"name": "Lisa Yang", "role": "Developer", "img": "https://imgur.com/oj7sy8j.jpg"},
    {"name": "Lynne Zheng", "role": "Developer", "img": "https://imgur.com/YATS2cD.jpg"},
]

for col, member in zip(cols, team):
    with col:
        st.markdown(f"""
            <div class="team-card">
                <img src="{member['img']}" alt="{member['name']}"/>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <h5 style="color: #000000; margin: 0.5rem 0 0.25rem 0;">{member['name']}</h5>
                    <p style="color: #000000; font-weight: 500; margin: 0;">{member['role']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)