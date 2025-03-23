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
    st.warning("This site can be only accessed by students.")
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

# Streamlit UI
st.title("📌 My Tutoring Requests")

requests = get_student_requests(username)

# Categorize requests
completed_requests = [req for req in requests if req.completed == 1]
uncompleted_requests = [req for req in requests if req.completed == 0]

request_categories = {
    f"✅ Completed Requests ({len(completed_requests)})": completed_requests,
    f"🟡 Uncompleted Requests ({len(uncompleted_requests)})": uncompleted_requests,
}

if not requests:
    st.info("No tutoring requests sent yet.")
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
