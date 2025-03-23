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
if st.session_state["role"] != "Tutor":
    st.warning("This site can be only accessed by tutors.")
    st.stop()

load_dotenv()

schema_name = "emoryhackathon"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# Get the tutor's ID in this session
username = st.session_state["username"]

# Function to fetch tutoring requests for a specific tutor
def get_tutoring_requests(tutor_id):
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tr.request_id, tr.student_user_id, tr.`status`, tr.message,
            s.name, s.university, s.graduation_year, s.major, s.employed_status, s.internships, s.grad_school, s.gpa_range, s.classes_taking, s.bio, s.email 
        FROM requests tr
        JOIN student s ON tr.student_user_id = s.user_id
        WHERE tr.tutor_user_id = :tutor_id;
        """)
        result = conn.execute(query, {"tutor_id": tutor_id}).fetchall()
    
    return result

# Function to update the request status
def update_request_status(request_id, new_status):
    with engine.connect() as conn:
        query = text("""
            UPDATE requests
            SET status = :new_status
            WHERE request_id = :request_id;
        """)
        conn.execute(query, {"new_status": new_status, "request_id": request_id})
        conn.commit()

# Streamlit UI
st.title("📌 Tutoring Requests")

requests = get_tutoring_requests(username)

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
    st.info("No tutoring requests received yet.")
else:
    for category, req_list in request_categories.items():
        with st.expander(category, expanded=False):
            if not req_list:
                st.write("No requests in this category.")
            else:
                for req in req_list:
                    # Display each request as a formatted block instead of an expander
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
                    
                    # Status selection dropdown
                    status_options = ["Pending", "Accepted", "Rejected"]
                    selected_status = st.selectbox(
                        "📌 Status:",
                        status_options,
                        index=status_options.index(req.status),
                        key=f"status_{req.request_id}"
                    )

                    # Update status if changed
                    if selected_status != req.status:
                        update_request_status(req.request_id, selected_status)
                        st.success(f"Status updated to {selected_status}.")