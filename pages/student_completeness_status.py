import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()
    
# Check login status
if st.session_state["role"] != "Student":
    st.warning("This page can only be accessed by students.")
    st.stop()

load_dotenv()

schema_name = "emoryhackathon"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# Get the student's ID in this session
username = st.session_state["username"]

# Function to fetch tutoring requests made by the student
def get_student_requests(student_id):
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tr.request_id, tr.tutor_user_id, tr.status, tr.completed,
            t.name, t.university, t.graduation_year, t.major, t.email
        FROM requests tr
        JOIN tutor t ON tr.tutor_user_id = t.user_id
        WHERE tr.student_user_id = :student_id;
        """)
        result = conn.execute(query, {"student_id": student_id}).fetchall()
    
    return result

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

# Streamlit UI
st.title("✅ Tutor Requests Completion Status")

requests = get_student_requests(username)

# Categorize requests
completed_requests = [req for req in requests if req.completed == 1]
uncompleted_requests = [req for req in requests if req.completed == 0]

request_categories = {
    f"✅ Completed Requests ({len(completed_requests)})": completed_requests,
    f"🟡 Uncompleted Requests ({len(uncompleted_requests)})": uncompleted_requests,
}

if not requests:
    st.info("You haven't sent any tutoring requests yet.")
else:
    for category, req_list in request_categories.items():
        with st.expander(category, expanded=False):
            if not req_list:
                st.write("No requests in this category.")
            else:
                for req in req_list:
                    st.markdown("---")
                    st.markdown(f"### 🔹 {req.name} — 📚 {req.major}, 🎓 {req.graduation_year}")
                    st.markdown(f"""
                    **🏫 University:** {req.university or 'N/A'}  
                    **📧 Email:** {req.email or 'N/A'}  
                    **📌 Status:** {req.status}  
                    """)
