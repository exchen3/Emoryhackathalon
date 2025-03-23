import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()

st.set_page_config(page_title="Find Tutor", layout="wide")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] == "Tutor":
    st.warning("This page can only be accessed by students.")
    st.stop()

username = st.session_state["username"]

# Create a session factory
schema_name = "emoryhackathon"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# ---- Navbar ----
st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
# st.markdown('<div class="navbar-title">TutorConnect</div>', unsafe_allow_html=True)

def logout():
    # Clear session state
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("You have been logged out.")
    time.sleep(1)
    st.switch_page("login.py")  # Navigate to login page
    
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

# Get distinct majors from the tutor table
def get_majors():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT major FROM tutor"))
        majors = [row[0] for row in result.fetchall()]
        return ["All"] + majors

# Get universities
def get_universities():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT university FROM tutor"))
        universities = [row[0] for row in result.fetchall()]
        return ["All"] + universities

# Get price ranges
def get_price_ranges():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT price_per_hour FROM tutor"))
        price_ranges = [row[0] for row in result.fetchall()]
        return ["All"] + price_ranges

# Get tutors based on selected filters
def get_tutors(selected_major_, selected_university_, selected_price_range_):
    with engine.connect() as conn:
        query = "SELECT user_id, name, university, graduation_year, major, classes_teaching, bio, email, price_per_hour FROM tutor WHERE 1=1"
        if selected_major_ != "All":
            query += f" AND major = '{selected_major_}'"
        if selected_university_ != "All":
            query += f" AND university = '{selected_university_}'"
        if selected_price_range_ != "All":
            query += f" AND price_per_hour = '{selected_price_range_}'"
        
        text_query = text(query)
        result = conn.execute(text_query).fetchall()
        return result

# Function to check if an active request exists
def active_request_exists(student_id, tutor_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM requests
            WHERE student_user_id = :student_id AND tutor_user_id = :tutor_id AND completed = 0
        """), {"student_id": student_id, "tutor_id": tutor_id}).scalar()
    return result > 0  # Returns True if an active request exists, False otherwise

# Function to send a tutoring request
def send_tutoring_request(student_id, tutor_id, message):
    if active_request_exists(student_id, tutor_id):
        st.warning("❗ You have an ongoing request with this tutor.")
    else:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO requests (student_user_id, tutor_user_id, status, message, completed)
                VALUES (:student_id, :tutor_id, 'Pending', :message, 0)
            """), {"student_id": student_id, "tutor_id": tutor_id, "message": message})
            conn.commit()
        st.success(f"✅ Request sent to {tutor_id}!")

# Streamlit UI
st.title("🎓 Finding a Tutor")

selected_major = st.selectbox("🔍 Select a Major", get_majors(), key="select_major")
selected_university = st.selectbox("🔍 Select a University", get_universities(), key="select_university")
selected_price_range = st.selectbox("🔍 Select a Price Range", get_price_ranges(), key="select_price_range")

# Show tutors
st.subheader("📌 Available Tutors")

tutors = get_tutors(selected_major, selected_university, selected_price_range)

if not tutors:
    st.info("No tutors found.")
else:
    for tutor in tutors:
        tutor_id, name, university, grad_year, major, classes_teaching, bio, email, price_per_hour = tutor

        with st.expander(f"🔹 {name} — {university or 'N/A'} ({grad_year or 'N/A'})"):
            st.markdown(f"📚 **Major:** {major or 'N/A'}")
            st.markdown(f"📝 **Classes Teaching:** {classes_teaching or 'N/A'}")
            st.markdown(f"💡 **Bio:** {bio or 'N/A'}")
            st.markdown(f"📧 **Email:** {email or 'N/A'}")

            # Message text area
            message = st.text_area(
                f"Message to {name}",
                max_chars=1000,
                placeholder="Write a short message to introduce yourself or explain what you need help with.",
                key=f"message_{tutor_id}"
            )

            # Request button
            if st.button(f"Request Tutoring from {name}", key=f"request_{tutor_id}"):
                student_id = st.session_state.get("username")
                if not student_id:
                    st.error("❌ You must be logged in to send a request.")
                elif not message.strip():
                    st.warning("Please write a message before submitting your request.")
                else:
                    send_tutoring_request(student_id, tutor_id, message)
