# 📚 TutorConnect

**TutorConnect** is a web-based platform built for a hackathon that connects underclassmen college students with qualified upperclassmen tutors. The goal is to offer flexible, peer-based academic support while also providing upperclassmen with gig-based income opportunities.

---

## 💡 Overview

**TutorConnect** solves two key problems:
- Helps underclassmen find approachable, relatable tutors from their own university or similar backgrounds.
- Provides upperclassmen with a flexible side gig opportunity by offering tutoring services in subjects they excel in.

The platform supports:
- Student & tutor onboarding
- Tutor discovery & filtering
- Request sending, management, and tracking
- Profile editing and completion tracking
- Role-based navigation and permissions

---

## 🚀 Features

### 🎓 For Students:
- View and edit your profile
- Browse and filter tutors by subject, school, or hourly rate
- Send tutoring requests with a personalized message
- Track status of each request (pending, accepted, rejected)
- View completion progress with each tutor

### 📘 For Tutors:
- Complete and update your tutoring profile
- View incoming tutoring requests from students
- Accept or reject requests
- Track completed tutoring sessions

---

## 🛠️ Tech Stack

| Layer        | Tools Used                             |
|-------------|-----------------------------------------|
| Frontend     | [Streamlit](https://streamlit.io/)     |
| Backend      | Python, SQLAlchemy                     |
| Database     | MySQL (via `pymysql`)                  |
| Styling      | HTML + CSS (via Streamlit markdown)    |
| Authentication | Simple session state (Streamlit native) |
| Config Management | `python-dotenv`                   |

---

## 📂 Directory Structure

- `login.py` — User login & role-based routing.
- `student_home_page.py`, `student_profile.py`, `student_info_input.py`, `find_tutor.py` — Pages for student workflows.
- `tutor_home_page.py`, `tutor_profile.py`, `tutor_info_input.py` — Pages for tutor workflows.
- `student_request_record.py`, `tutor_request_list.py` — Request management dashboards.
- `tutor_completeness_status.py`, `student_completeness_status.py` — Completion tracking for tutors and students.

---

## 🧪 How to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file with:
   ```
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   ```

3. **Run Streamlit**
   ```bash
   streamlit run login.py
   ```

---

## ⚠️ Notes

- The app uses Streamlit’s `st.session_state` to manage login state and role-based permissions.
- Ensure your MySQL database (`emoryhackathon`) is populated with appropriate `student`, `tutor`, and `requests` tables.
- Foreign key constraints must be handled carefully (especially when modifying `user_id`).

---

## 👥 Team

Built by a group of Emory University students for a hackathon competition.  
Main contributors include: Andy Dang, Eric Chen, Lisa Yang, and Lynne Zheng.
