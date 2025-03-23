import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] != "Tutor":
    st.warning("This site can be only accessed by tutors.")
    st.stop()

# Set page config
st.set_page_config(page_title="Tutor Profile", layout="centered")

username = st.session_state["username"]

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
            if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
                st.warning("Please log in first!")
                st.switch_page("login.py")
            else:
                role = st.session_state.get("role")
                if role == "Student":
                    st.switch_page("pages/student_profile.py")
                elif role == "Tutor":
                    st.switch_page("pages/tutor_profile.py")

    with col_links[2]:
        if st.button("🎓 Tutors", use_container_width=True):
            st.switch_page("pages/find_tutor.py")


    def logout():
        # Clear session state
        for key in ["logged_in", "username", "role"]:
            if key in st.session_state:
                del st.session_state[key]
    with col_links[3]:
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")
schema_name = "emoryhackathon"

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

with engine.connect() as conn:
    retrieve_query = text(f"SELECT * FROM tutor WHERE user_id = '{username}'")
    result = conn.execute(retrieve_query).fetchone()


# Sample tutor data (replace with your DB query)
tutor = {
    "name": result[2],
    "university": result[3],
    "graduation_year": result[4],
    "employed_status": result[6],
    "grad_school": result[8],
    "major": result[5],
    "gpa_range": result[9],
    "classes_teaching": result[10],
    "bio": result[11],
    "email": result[12]
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

if st.button("Edit Your Tutor Profile"):
    st.switch_page("pages/tutor_info_input.py")

st.markdown('</div>', unsafe_allow_html=True)