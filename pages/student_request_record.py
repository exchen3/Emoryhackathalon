import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()
    
# Check login status
if st.session_state["role"] != "Student":
    st.warning("This page is only accessible by students.")
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

# Streamlit UI
st.title("📌 Your Tutoring Requests")

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
