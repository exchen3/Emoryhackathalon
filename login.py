import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import hashlib
import time

# Set page configuration
st.set_page_config(page_title="Login", layout="wide")

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","localhost")

schema_name = "emoryhackathon"

### Debug
# print("DEBUG ENV:")
# print("DB_USERNAME =", os.getenv("DB_USERNAME"))
# print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))
# print("DB_HOST =", os.getenv("DB_HOST"))

# ---- Navbar ----
st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
# st.markdown('<div class="navbar-title">TutorConnect</div>', unsafe_allow_html=True)

# Use Streamlit's built-in page links for navigation
with st.container():
    col_links = st.columns(3)

    with col_links[1]:
        if st.button("🧭 About Us", use_container_width=True):
            st.switch_page("pages/about_us.py")

# Construct the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{schema_name}?host={DB_HOST}")

## TODO: Make login function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select your role", ["Student", "Tutor"], key = "role_info")

    if st.button("Login"):
        if not username or not password or not role:
            st.error("Please enter both username and password.")
            return

        hashed_password = hash_password(password)

        try:
                with engine.connect() as conn:
                    query = text(f"SELECT password FROM {role} WHERE user_id = :username")
                    result = conn.execute(query, {"username": username}).fetchone()

                    if result and result[0] == hashed_password:
                        st.success(f"Welcome, {username}!")

                        # Store user login state
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = role


                        # Redirect to according info page
                        if role == "Student":
                            check_query = text(
                                f"SELECT email IS NULL FROM student WHERE user_id = '{st.session_state['username']}'"
                            )

                            is_empty = conn.execute(check_query).fetchone()

                            if is_empty and is_empty[0]:
                                st.switch_page("pages/student_info_input.py")
                            else:
                                st.switch_page("pages/student_home_page.py")
                        elif role == "Tutor":
                            check_query = text(
                                f"SELECT email IS NULL FROM tutor WHERE user_id = '{st.session_state['username']}'"
                            )
                            is_empty = conn.execute(check_query).fetchone()
                            if is_empty and is_empty[0]:
                                st.switch_page("pages/tutor_info_input.py")
                            else:
                                st.switch_page("pages/tutor_home_page.py")
                    else:    
                        st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Database error: {e}")


def register():
    st.title("Register New Account")

    new_username = st.text_input("Username", key="reg_username")
    new_full_name = st.text_input("Name", key="reg_full_name")
    new_password = st.text_input("Choose a Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    new_role = st.selectbox("Select your role", ["Student", "Tutor"], key = "new_role")

    if st.button("Register"):
        if not new_username or not new_password or not confirm_password or not new_role:
            st.error("All fields are required.")
            return
        
        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return

        hashed_password = hash_password(new_password)

        try:
            with engine.connect() as conn:
                # Check if username already exists
                check_query = text(f"SELECT user_id FROM {new_role} WHERE user_id = :username")
                existing_user = conn.execute(check_query, {"username": new_username}).fetchone()

                if existing_user:
                    st.error("Username already exists. Please choose another.")
                    return

                # Insert new user
                insert_query = text(f"""
                    INSERT INTO {new_role} (user_id, password, name,major)
                    VALUES (:username, :password, :user_name, :major)
                """)
                conn.execute(insert_query, {
                    "username": new_username,
                    "password": hashed_password,
                    "user_name": new_full_name,
                    "major": "Undeclared"
                })

                conn.commit()

                st.success("Registration successful! You can now log in.")

        except Exception as e:
            st.error(f"Database error: {e}")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.success(f"Welcome back, {st.session_state['username']}!")

else:
    tab1, tab2 = st.tabs(["Login", "Create a New Account"])

    with tab1:
        login()

    with tab2:
        register()