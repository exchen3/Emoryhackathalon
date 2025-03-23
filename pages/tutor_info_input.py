import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

# Set page configuration
# st.set_page_config(page_title="Tutor Info Input", layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    if st.button("Login Page", use_container_width=True):
        st.switch_page("login.py")
    st.stop()

if st.session_state["role"] != "Tutor":
    st.warning("This page can only be accessed by tutors.")
    st.stop()

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

schema_name = "emoryhackathon"

# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{schema_name}")

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first!")
    st.stop()

# Retrieve username from session
username = st.session_state.get("username")

st.title("🎓 Tutor Connect - Tutor Registration")

def personal_information(user_id=username):
    # Fetch current values from the DB
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM tutor WHERE user_id = :username")
            result = conn.execute(query, {"username": user_id}).fetchone()

            if result:
                current_info = result._mapping
            else:
                st.error("No tutor record found for this user.")
                return
    except Exception as e:
        st.error(f"Database error fetching current data: {e}")
        return

    # Set default values from DB or show placeholder if empty
    email = st.text_input(
        "Enter your Email",
        value=current_info.get("email") or "",
        key="email"
    )
    universities = [
        "Amherst College",
        "Arizona State University",
        "Babson College",
        "Bard College",
        "Barnard College",
        "Baylor University",
        "Boston College",
        "Boston University",
        "Bowdoin College",
        "Brandeis University",
        "Brown University",
        "California Institute of Technology (Caltech)",
        "Carnegie Mellon University",
        "Colby College",
        "Columbia University",
        "Cornell University",
        "Dartmouth College",
        "Duke University",
        "Emory University",
        "Florida State University",
        "Georgetown University",
        "Georgia Institute of Technology",
        "Harvard University",
        "Indiana University Bloomington",
        "Johns Hopkins University",
        "Louisiana State University",
        "Massachusetts Institute of Technology (MIT)",
        "Northwestern University",
        "Ohio State University",
        "Oregon State University",
        "Princeton University",
        "Purdue University",
        "Rice University",
        "Stanford University",
        "Syracuse University",
        "Temple University",
        "Texas A&M University",
        "The George Washington University",
        "The New School",
        "Tufts University",
        "University of California, Berkeley",
        "University of California, Los Angeles (UCLA)",
        "University of Chicago",
        "University of Florida",
        "University of Illinois Urbana-Champaign",
        "University of Maryland, College Park",
        "University of Michigan",
        "University of North Carolina at Chapel Hill",
        "University of Notre Dame",
        "University of Pennsylvania",
        "University of Pittsburgh",
        "University of Southern California (USC)",
        "University of Texas at Austin",
        "University of Washington",
        "Vanderbilt University",
        "Wake Forest University",
        "Washington University in St. Louis",
        "Wellesley College",
        "Yale University"
        "Other",
    ]

    university = st.selectbox(
        "Select Your University",
        universities,
        index = universities.index(current_info.get("university")) if current_info.get("university") in universities else 0,
        key="university"
    )
    grad_year = st.number_input(
        "Graduation Year", 
        min_value=1990, 
        max_value=2035, 
        step=1, 
        value=current_info.get("graduation_year"), 
        key="grad_year"
    )
    majors = [
        "Biology", "Chemistry", "Physics", "Mathematics", "Statistics",
        "Computer Science", "Data Science", "Engineering", "Psychology",
        "Economics", "Business", "Finance", "Accounting", "Marketing",
        "History", "Political Science", "Philosophy", "Sociology", "Anthropology",
        "English", "Linguistics", "Education", "Communication", "Journalism",
        "Law", "Criminal Justice", "Public Policy",
        "Medicine", "Nursing", "Public Health", "Pharmacy", "Neuroscience",
        "Environmental Science", "Geology", "Astronomy", "Agricultural Science",
        "Art", "Music", "Theater", "Film Studies", "Graphic Design",
        "Sports Management", "Kinesiology",
        "Other"
    ]

    major = st.selectbox(
        "Select your Major", 
        majors, 
        index=majors.index(current_info.get("major")) if current_info.get("major") in majors else 0,
        key="major"
    )
    employed_status = st.checkbox(
        "Currently Employed?", 
        value=bool(current_info.get("employed_status")), 
        key="employed_status"
    )
    internships = st.checkbox(
        "Have you done any Internships?", 
        value=bool(current_info.get("internships")), 
        key="internships"
    )
    grad_school = st.checkbox(
        "Are you currently in Graduate School?", 
        value=bool(current_info.get("grad_school")), 
        key="grad_school"
    )
    gpa_options = ["Below 2.5", "2.5 - 3.0", "3.0 - 3.5", "3.5 - 4.0"]
    gpa_range = st.selectbox(
        "Select your GPA Range (on a scale of 4)", 
        gpa_options, 
        index=gpa_options.index(current_info.get("gpa_range")) if current_info.get("gpa_range") in gpa_options else 0,
        key="gpa_range"
    )
    classes_teaching = st.text_area(
        "Enter the classes want to teach (comma-separated)", 
        value=current_info.get("classes_teaching"), 
        key="classes_teaching"
    )
    price_options = ['under 20',
                    '20-30',
                    '30-40',
                    '40-50',
                    '50-60',
                    '60-70',
                    '70-80',
                    '80-90',
                    '90-100',
                    'over 100']
    price_per_hour = st.selectbox(
        "Choose the ideal price range",
        price_options,
        index= price_options.index(current_info.get("gpa_range")) if current_info.get("price_per_hour") in gpa_options else 0,
        key = "price_per_hour"
    )
    bio = st.text_area(
        "Write a short bio about yourself", 
        value=current_info.get("bio"), 
        key="bio"
    )

    # Submit updated info
    if st.button("Submit Information"):
        # Check required fields
        if not university or university == "empty" or not classes_teaching or classes_teaching == "empty" or not bio or bio == "empty" or not price_per_hour or price_per_hour == "empty":
            st.warning("Please fill in all required fields.")
            return

        try:
            with engine.connect() as conn:
                modify_query = text("""                                
                    UPDATE tutor
                    SET university = :university, 
                        graduation_year = :grad_year, 
                        major = :major, 
                        employed_status = :employed_status,
                        internships = :internships, 
                        grad_school = :grad_school, 
                        gpa_range = :gpa_range, 
                        classes_teaching = :classes_teaching, 
                        bio = :bio,
                        email = :email
                    WHERE user_id = :username
                ;""")

                conn.execute(modify_query, {
                    "university": university,
                    "grad_year": grad_year,
                    "major": major,
                    "employed_status": employed_status,
                    "internships": internships,
                    "grad_school": grad_school,
                    "gpa_range": gpa_range,
                    "classes_teaching": classes_teaching,
                    "bio": bio,
                    "username": user_id,
                    "email": email
                })

                conn.commit()
                st.success("Personal Information Updated!")
                
                st.page_link("pages/tutor_home_page.py", label="Go to Tutor Home Page")

                # st.markdown('<meta http-equiv="refresh" content="0; url=http://localhost:8501/student_home_page.html">', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Database error: {e}")


st.header("Fill in or Edit Your Personal Information")
personal_information()