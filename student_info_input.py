import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import subprocess
import base64

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

schema_name = "emoryhackathon"
engine = create_engine(f"mysql+pymysql://root:{DB_PASSWORD}@{DB_HOST}/{schema_name}")

# Set page configuration
st.set_page_config(page_title="Info Input", layout="wide")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    st.stop()

# Retrieve username from session
username = st.session_state.get("username")

st.title("🎓 Alumni Connect - Student Registration")

def personal_information(user_id = username):
    # User input fields
    university = st.text_input("Enter your University")
    grad_year = st.number_input("Graduation Year", min_value=1990, max_value=2035, step=1)

    # Standardized list of majors
    majors = ["Computer Science", "Biology", "Business", "Engineering", "Psychology", "Other"]
    major = st.selectbox("Select your Major", majors)

    # Boolean selections
    employed_status = st.checkbox("Currently Employed?")
    internships = st.checkbox("Have you done any Internships?")
    grad_school = st.checkbox("Are you current in Graduate School?")

    # GPA range selection
    gpa_options = ["Below 2.5", "2.5 - 3.0", "3.0 - 3.5", "3.5 - 4.0", "4.0+"]
    gpa_range = st.selectbox("Select your GPA Range", gpa_options)

    # Classes Taking (comma-separated input)
    classes_taking = st.text_area("Enter the classes you are taking (comma-separated)")

    # Personal Bio
    bio = st.text_area("Write a short bio about yourself")

    try:
        with engine.connect() as conn:
            # Insert new user
            modify_query = text("""
                INSERT INTO customers (user_id, password, user_name, favorites, last_visit)
                VALUES (:username, :password, :user_name, NULL, CURDATE())
                                
                UPDATE student
                SET university = :university, 
                    graduation_year = :grad_year, 
                    major = :major, 
                    employed_status = :employed_status,
                    internships = :internships, 
                    grad_school = :grad_school, 
                    gpa_range = :gpa_range, 
                    classes_taking = :classes_taking, 
                    bio = :bio
                WHERE user_id = :username
            ;
            """)

            conn.execute(modify_query, {
                "university": university,
                "grad_year": grad_year,
                "major": major,
                "employed_status": employed_status,
                "internships": internships,
                "grad_school": grad_school,
                "gpa_range": gpa_range, 
                "classes_taking": classes_taking, 
                "bio": bio,
                "username": user_id
            })

            conn.commit()

            st.success("Personal Information Updated!")

    except Exception as e:
        st.error(f"Database error: {e}")

# TODO: remove the 2nd tab
tab1, tab2 = st.tabs(["Fill in Personal Information", "Edit Existing Personal Information"])

with tab1:
    personal_information()
with tab2:
    personal_information()