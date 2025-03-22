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


# Function to fetch tutoring requests for a specific tutor
def get_tutoring_requests(tutor_id):
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tr.request_id, tr.tutor_id, tr.student_id, tr.status, tr.message,
            s.name, s.major, s.grad_year
        FROM tutoring_requests tr
        JOIN students s ON tr.student_id = s.student_id
        WHERE tr.tutor_id = :tutor_id;
        """)
        result = conn.execute(query, {"tutor_id": tutor_id}).fetchall()

    if not result:
        st.write("No tutoring requests at the moment.")
    else:
        # Horizontal scrolling request cards
        html_code = """
        <style>
            .scroll-container {
                display: flex;
                overflow-x: auto;
                gap: 20px;
                padding: 10px;
                white-space: nowrap;
            }
            .card {
                flex: 0 0 auto;
                width: 250px;
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                text-align: left;
            }
        </style>
        <div class="scroll-container">
        """

        for req in result:
            request_id, tutor_id, student_id, status, message, name, major, grad_year = req
            html_code += f"""
            <div class="card">
                <h4>{name}</h4>
                <p><b>Major:</b> {major}</p >
                <p><b>Graduation Year:</b> {grad_year}</p >
                <p><b>Message:</b> {message}</p >
                <p><b>Status:</b> {status}</p >
                <div class="button-container">
                    <button class="accept-btn" onclick="acceptRequest({request_id})">Accept</button>
                    <button class="reject-btn" onclick="rejectRequest({request_id})">Reject</button>
                </div>
            </div>
            """

        html_code += "</div>"


# Mock user login (replace with actual authentication logic)
tutor_id = 1  # Example tutor ID; dynamically replace this

# Fetch tutoring requests for the logged-in tutor
tutoring_requests = get_tutoring_requests(tutor_id)

# Streamlit UI
st.title("Tutoring Requests")

if not tutoring_requests:
    st.write("No tutoring requests at the moment.")
else:
    # Horizontal scrolling request cards
    html_code = """
    <style>
        .scroll-container {
            display: flex;
            overflow-x: auto;
            gap: 20px;
            padding: 10px;
            white-space: nowrap;
        }
        .card {
            flex: 0 0 auto;
            width: 250px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: left;
        }
    </style>
    <div class="scroll-container">
    """

    for req in tutoring_requests:
        request_id, tutor_id, student_id, status, message, name, major, grad_year = req
        html_code += f"""
        <div class="card">
            <h4>{name}</h4>
            <p><b>Major:</b> {major}</p >
            <p><b>Graduation Year:</b> {grad_year}</p >
            <p><b>Message:</b> {message}</p >
            <p><b>Status:</b> {status}</p >
            <div class="button-container">
                <button class="accept-btn" onclick="acceptRequest({request_id})">Accept</button>
                <button class="reject-btn" onclick="rejectRequest({request_id})">Reject</button>
            </div>
        </div>
        """

    html_code += "</div>"

    st.components.html(html_code, height=300)