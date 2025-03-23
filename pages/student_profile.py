import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()
# Page configuration
st.set_page_config(page_title="Student Profile", layout="wide")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] != "Student":
    st.warning("This page can only be accessed by students.")
    st.stop()

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

st.title("🧑 Student Profile")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")

schema_name = "emoryhackathon"

# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")
username = st.session_state["username"]

retrieve_query = text(f"SELECT * FROM student WHERE user_id = '{username}'")
with engine.connect() as conn:
    result = conn.execute(retrieve_query).fetchone()

try:
    with engine.connect() as conn:
        query = text(f"SELECT * FROM student WHERE user_id = :username")
        result = conn.execute(query, {"username": username}).fetchone()

except Exception as e:
    st.error(f"Database error: {e}")  

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

# # Profile content
# st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
# st.markdown('<div class="navbar-title">TutorConnect</div>', unsafe_allow_html=True)

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
if st.button("Edit Your Student Profile"):
    st.switch_page("pages/student_info_input.py")

st.markdown('</div>', unsafe_allow_html=True)  # End of profile-container