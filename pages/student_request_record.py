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

# Function to fetch requests sent by the student
def get_student_requests(student_id):
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tr.request_id, tr.tutor_user_id, tr.`status`, tr.message,
            t.name, t.university, t.graduation_year, t.major, t.employed_status, t.internships, t.grad_school, t.gpa_range, t.classes_teaching, t.bio, t.email 
        FROM requests tr
        JOIN tutor t ON tr.tutor_user_id = t.user_id
        WHERE tr.student_user_id = :student_id;
        """)
        result = conn.execute(query, {"student_id": student_id}).fetchall()
    
    return result


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
    text-align: center;
    padding: 2rem 1rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    color: black; /* 👈 Add this */
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

# Streamlit UI

def logout():
    # Clear session state
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]

    st.success("You have been logged out.")
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

st.title("📌 Requests Sent to Tutors")
requests = get_student_requests(username)

# Categorize requests
pending_requests = [req for req in requests if req.status == "Pending"]
accepted_requests = [req for req in requests if req.status == "Accepted"]
rejected_requests = [req for req in requests if req.status == "Rejected"]

request_categories = {
    f"🟡 Pending Requests ({len(pending_requests)})": pending_requests,
    f"🟢 Accepted Requests ({len(accepted_requests)})": accepted_requests,
    f"🔴 Rejected Requests ({len(rejected_requests)})": rejected_requests,
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
                    # Display each request as a formatted block
                    st.markdown("---")
                    st.markdown(f"### 🔹 {req.name} — 📚 {req.major}, 🎓 {req.graduation_year}")
                    st.markdown(f"""
                    **🏫 University:** {req.university or 'N/A'}  
                    **💼 Employment Status:** {'Employed' if req.employed_status else 'Not Employed'}  
                    **🛠️ Internship Experience:** {'Yes' if req.internships else 'No'}  
                    **🎓 Graduate School Plans:** {'Yes' if req.grad_school else 'No'}  
                    **📊 GPA Range:** {req.gpa_range or 'N/A'}  
                    **📖 Classes Teaching:** {req.classes_teaching or 'N/A'}  
                    **💡 Bio:** {req.bio or 'N/A'}  
                    **📧 Email:** {req.email or 'N/A'}  
                    """)

                    st.markdown(f"✉️ **Your Message:** {req.message}")
                    st.markdown(f"📌 **Status:** `{req.status}`")
