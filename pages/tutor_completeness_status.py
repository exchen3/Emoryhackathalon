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
if st.session_state["role"] != "Tutor":
    st.warning("This page can only be accessed by tutors.")
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
    col_links = st.columns(6)

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
        if st.button("📌 Request List", use_container_width=True):
            st.switch_page("pages/tutor_request_list.py")

    with col_links[4]:
        if st.button("✅ Request Completion", use_container_width=True):
            st.switch_page("pages/tutor_completeness_status.py")

    with col_links[5]:
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()


load_dotenv()

schema_name = "emoryhackathon"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# Get the tutor's ID in this session
username = st.session_state["username"]

# Function to fetch accepted tutoring requests

def get_accepted_requests(tutor_id):
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tr.request_id, tr.student_user_id, tr.completed, tr.message,
            s.name, s.university, s.graduation_year, s.major, s.employed_status, s.internships, s.grad_school, s.gpa_range, s.classes_taking, s.bio, s.email 
        FROM requests tr
        JOIN student s ON tr.student_user_id = s.user_id
        WHERE tr.tutor_user_id = :tutor_id AND tr.status = 'Accepted';
        """)
        result = conn.execute(query, {"tutor_id": tutor_id}).fetchall()
    
    return result

# Function to update completion status
def update_completion_status(request_id, new_status):
    with engine.connect() as conn:
        query = text("""
            UPDATE requests
            SET completed = :new_status
            WHERE request_id = :request_id;
        """)
        conn.execute(query, {"new_status": new_status, "request_id": request_id})
        conn.commit()

# Streamlit UI
st.title("✅ Tutor Requests Completion Status")

requests = get_accepted_requests(username)

# Categorize requests
uncompleted_requests = [req for req in requests if req.completed == 0]
completed_requests = [req for req in requests if req.completed == 1]

request_categories = {
    f"🟠 Uncompleted Requests ({len(uncompleted_requests)})": uncompleted_requests,
    f"🟢 Completed Requests ({len(completed_requests)})": completed_requests,
}

if not requests:
    st.info("No accepted tutoring requests yet.")
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
                    **💼 Employment Status:** {'Employed' if req.employed_status else 'Not Employed'}  
                    **🛠️ Internship Experience:** {'Yes' if req.internships else 'No'}  
                    **🎓 Graduate School Plans:** {'Yes' if req.grad_school else 'No'}  
                    **📊 GPA Range:** {req.gpa_range or 'N/A'}  
                    **📖 Classes Taking:** {req.classes_taking or 'N/A'}  
                    **💡 Bio:** {req.bio or 'N/A'}  
                    **📧 Email:** {req.email or 'N/A'}  
                    """)

                    st.markdown(f"✉️ **Message:** {req.message}")
                    
                    # Completion status selection dropdown
                    completion_options = ["Uncompleted", "Completed"]
                    selected_completion = st.selectbox(
                        "✅ Completion Status:",
                        completion_options,
                        index=completion_options.index("Completed") if req.completed else 0,
                        key=f"completion_{req.request_id}"
                    )
                    
                    # Update status if changed
                    new_status_value = 1 if selected_completion == "Completed" else 0
                    if new_status_value != req.completed:
                        update_completion_status(req.request_id, new_status_value)
                        st.success(f"Completion status updated to {selected_completion}.")
