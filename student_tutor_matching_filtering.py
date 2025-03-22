import streamlit as st
from sqlalchemy import text
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Create a session factory
schema_name = "emoryhackathon"

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

# SessionLocal = sessionmaker(bind=engine)

# Fetch available majors
def get_majors():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT major FROM tutor"))
        return ["All"] + [row[0] for row in result.fetchall()]

# Fetch tutors based on the selected major
def get_tutors(selected_major):
    with engine.connect() as conn:
        if selected_major == "All":
            result = conn.execute(text("SELECT * FROM tutor"))
        else:
            result = conn.execute(text("SELECT * FROM tutor WHERE major = :major"), {"major": selected_major})
        return result.fetchall()

# Streamlit UI
st.title("🎓 Tutor-Student Matching System")

# 1️⃣ Student selects a major (question category)
selected_major = st.selectbox("🔍 Select a Major", get_majors())

# 2️⃣ Show tutors who match the major
tutors = get_tutors(selected_major)

st.subheader("📌 Available Tutors")
for tutor in tutors:
    tutor_id, name, university, grad_year, major, classes_teaching, bio = tutor
    with st.expander(f"🔹 {name} - {university} ({grad_year})"):
        st.markdown(f"📚 **Major:** {major}")
        st.markdown(f"📝 **Classes Teaching:** {classes_teaching}")
        st.markdown(f"💡 **Bio:** {bio}")

        # 3️⃣ Students can submit a tutoring request
        if st.button(f"Request Tutoring from {name}", key=f"request_{tutor_id}"):
            with engine.connect() as conn:
                student_id = "sample_student_id"  # TODO: Replace with actual session user ID
                conn.execute(
                    text("INSERT INTO tutoring_requests (student_id, tutor_id, status) VALUES (:student_id, :tutor_id, 'Pending')"),
                    {"student_id": student_id, "tutor_id": tutor_id},
                )
                conn.commit()
            st.success(f"✅ Request sent to {name}!")
