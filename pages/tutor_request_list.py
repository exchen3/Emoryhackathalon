import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

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
            s.name, s.major, s.graduation_year
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

if not requests:
    st.info("No tutoring requests received yet.")
else:
    for req in requests:
        with st.expander(f"🔹 {req.name} — 📚 {req.major}, 🎓 {req.graduation_year}"):
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

