import streamlit as st
import requests

st.title("📚 Alumni Connect - Tutor Registration")

# User input fields
user_id = st.text_input("Enter your User ID (Email)")
password = st.text_input("Enter your Password", type="password")
name = st.text_input("Enter your Name")
university = st.text_input("Enter your University")
grad_year = st.number_input("Graduation Year", min_value=1990, max_value=2035, step=1)

# Standardized list of majors
majors = ["Computer Science", "Biology", "Business", "Engineering", "Psychology", "Other"]
major = st.selectbox("Select your Major", majors)

# Boolean selections
employed_status = st.checkbox("Currently Employed?")
internships = st.checkbox("Have you done any Internships?")
grad_school = st.checkbox("Planning for Graduate School?")

# GPA range selection
gpa_options = ["Below 2.5", "2.5 - 3.0", "3.0 - 3.5", "3.5 - 4.0", "4.0+"]
gpa_range = st.selectbox("Select your GPA Range", gpa_options)

# Classes Teaching (comma-separated input)
classes_taking = st.text_area("Enter the classes you can teach (comma-separated)")

# Personal Bio
bio = st.text_area("Write a short bio about yourself")

# Submit button
if st.button("Submit"):
    if user_id and password and name and university and grad_year and major and gpa_range and classes_taking and bio:
        tutor_data = {
            "user_id": user_id,
            "password": password,
            "name": name,
            "university": university,
            "graduation_year": grad_year,
            "major": major,
            "employed_status": employed_status,
            "internships": internships,
            "grad_school": grad_school,
            "gpa_range": gpa_range,
            "classes_taking": classes_taking,
            "bio": bio
        }
        
        response = requests.post("http://127.0.0.1:5000/register", json=tutor_data)
        
        if response.status_code == 200:
            st.success(f"Welcome, {name}! Your information has been recorded.")
        else:
            st.error("Error submitting your information. Please try again.")
    else:
        st.warning("Please fill out all required fields before submitting.")