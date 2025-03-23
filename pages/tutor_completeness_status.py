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
st.title("✅ Completion Status of Tutoring Requests")

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
