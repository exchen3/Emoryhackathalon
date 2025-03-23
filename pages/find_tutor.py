import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

username = st.session_state["username"]

# Create a session factory
schema_name = "emoryhackathon"

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# Get distinct majors from the tutor table
def get_majors():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT major FROM tutor"))
        majors = [row[0] for row in result.fetchall()]
        return ["All"] + majors  # Add "All" option to show all tutors

def get_universities():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT university FROM tutor"))
        universities = [row[0] for row in result.fetchall()]
        return ["All"] + universities

def get_price_ranges():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT price_per_hour FROM tutor"))
        price_ranges = [row[0] for row in result.fetchall()]
        return ["All"] + price_ranges

# Get tutors based on selected major
def get_tutors(selected_major_, selected_university_, selected_price_range_):
    with engine.connect() as conn:
        query = "SELECT user_id, name, university, graduation_year, major, classes_teaching, bio, email, price_per_hour FROM tutor WHERE 1=1"
        if selected_major_ != "All":
            query += f" AND major = '{selected_major_}'"
        if selected_university_ != "All":
            query += f" AND university = '{selected_university_}'"
        if selected_price_range_ != "All":
            query += f" AND price_per_hour = {selected_price_range_}"

        text_query = text(query)
        result = conn.execute(text_query).fetchall()
        return result

# Function to check if a request already exists
def request_exists(student_id, tutor_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM requests
            WHERE student_user_id = :student_id AND tutor_user_id = :tutor_id
        """), {"student_id": student_id, "tutor_id": tutor_id}).scalar()
    return result > 0  # Returns True if request exists, False otherwise

# Function to send a tutoring request
def send_tutoring_request(student_id, tutor_id, message):
    if request_exists(student_id, tutor_id):
        st.warning("❗ You have already sent a request to this tutor.")
    else:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO requests (student_user_id, tutor_user_id, status, message)
                VALUES (:student_id, :tutor_id, 'pending', :message)
            """), {"student_id": student_id, "tutor_id": tutor_id, "message": message})
            conn.commit()
        st.success(f"✅ Request sent to {tutor_id}!")

# Streamlit UI
st.title("🎓 Finding a Tutor")

# 1️⃣ Student selects a major (question category)
selected_major = st.selectbox("🔍 Select a Major", get_majors(), key="select_major")
selected_university = st.selectbox("🔍 Select a University", get_universities(), key="select_university")
selected_price_range = st.selectbox("🔍 Select a Price Range", get_price_ranges(), key="select_price_range")

# 2️⃣ Show tutors who match the major
tutors = get_tutors(selected_major, selected_university, selected_price_range)

st.subheader("📌 Available Tutors")

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

            # 💬 Message text area (unique key per tutor)
            message = st.text_area(
                f"Message to {name}",
                max_chars=1000,
                placeholder="Write a short message to introduce yourself or explain what you need help with.",
                key=f"message_{tutor_id}"
            )

            # 📩 Request button
            if st.button(f"Request Tutoring from {name}", key=f"request_{tutor_id}"):
                student_id = st.session_state.get("username")
                if not student_id:
                    st.error("❌ You must be logged in to send a request.")
                elif not message.strip():
                    st.warning("Please write a message before submitting your request.")
                else:
                    send_tutoring_request(student_id, tutor_id, message)