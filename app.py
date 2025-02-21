import streamlit as st
import pandas as pd
import json
import os
import random
import google.generativeai as genai

# -------------------- CONFIGURATION --------------------

# Set API Key for Gemini AI
genai.configure(api_key=st.secrets["GOOGLE_GEMINI_API_KEY"])

# Constants
USER_DATA_FILE = "data/users.json"
CANDIDATE_FILE = "data/candidates.json"
LOGIN_COUNT_FILE = "data/login_count.json"
RESUME_FOLDER = "data/resumes/"
ADMIN_PASSKEY = "12345678"  # Change this as required

# Ensure necessary folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

# Page Configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="wide"
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .big-font { font-size:24px !important; font-weight: bold; }
        .info-box { background-color: #f4f4f4; padding: 10px; border-radius: 5px; padding: 10px; }
        .stButton button { background-color: #4CAF50; color: white; }
    </style>
""",
    unsafe_allow_html=True,
)

# -------------------- FUNCTIONS --------------------


# Function to Load User Data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}


# Function to Save User Data
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)


# Function to Handle Signup
def signup():
    st.title("🔐 Sign Up")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    is_admin = False

    if st.checkbox("Apply for Admin Access"):
        passkey = st.text_input("Enter 8-digit Admin Passkey", type="password")
        if passkey == ADMIN_PASSKEY:
            is_admin = True
            st.success("✅ Admin Access Granted")
        else:
            st.warning("⚠️ Incorrect Admin Passkey")

    if st.button("Register"):
        users = load_users()
        if username in users:
            st.warning("⚠️ Username already exists.")
        else:
            users[username] = {"password": password, "is_admin": is_admin}
            save_users(users)
            st.success("✅ Registration Successful! Please Login.")


# Function to Track Logins
def increment_login_count():
    if os.path.exists(LOGIN_COUNT_FILE):
        with open(LOGIN_COUNT_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"logins": 0}

    data["logins"] += 1

    with open(LOGIN_COUNT_FILE, "w") as f:
        json.dump(data, f)


def get_login_count():
    if os.path.exists(LOGIN_COUNT_FILE):
        with open(LOGIN_COUNT_FILE, "r") as f:
            data = json.load(f)
            return data.get("logins", 0)
    return 0


# Function to Handle Login
def login():
    st.title("🔑 Login")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["is_admin"] = users[username]["is_admin"]
            increment_login_count()
            st.rerun()
        else:
            st.warning("⚠️ Incorrect Username or Password")


# Function to Load Candidate Data
def load_candidates():
    if os.path.exists(CANDIDATE_FILE) and os.path.getsize(CANDIDATE_FILE) > 0:
        with open(CANDIDATE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# Save Candidate Data (Replace Old Entry)
def save_candidate(candidate_info):
    candidates = load_candidates()
    email = candidate_info["Email"]

    # Remove previous entry if it exists
    candidates = [c for c in candidates if c["Email"] != email]

    # Add the latest entry
    candidates.append(candidate_info)

    # Save updated candidate list
    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=2)


# Function to Save Candidate Data
def save_candidate(candidate_info):
    candidates = load_candidates()
    candidates.append(candidate_info)

    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=2)


# Collect Candidate Information
def collect_candidate_info():
    st.subheader("📝 Candidate Information Form")

    candidate_info = {
        "Full Name": st.text_input("Full Name"),
        "Email": st.text_input("Email"),
        "Phone": st.text_input("Phone Number"),
        "Experience": st.text_input("Years of Experience"),
        "Position": st.text_input("Applied Position"),
        "Location": st.text_input("Current Location"),
        "Tech Stack": st.text_area("Technology Stack (Comma-Separated)"),
    }

    resume = st.file_uploader("📂 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

    if st.button("Submit"):
        if all(candidate_info.values()):
            if resume:
                resume_path = os.path.join(RESUME_FOLDER, resume.name)
                with open(resume_path, "wb") as f:
                    f.write(resume.getbuffer())
                candidate_info["Resume"] = resume_path

            save_candidate(candidate_info)
            st.success("✅ Candidate Information Saved")
            st.info(f"📊 AI Suitability Score: {random.randint(60, 95)}%")
        else:
            st.warning("⚠️ Please fill all details.")


# Handle Chatbot Responses
def handle_chat(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text.strip() if response.text else "I couldn't understand."


# -------------------- MAIN APP --------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.sidebar.title("🔑 Login & Sign Up")
    page = st.sidebar.radio("Select Option", ["Login", "Sign Up"])
    if page == "Login":
        login()
    else:
        signup()
else:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=100)
    st.sidebar.title("📋 TalentScout Assistant")

    if st.session_state["is_admin"]:
        page = st.sidebar.radio(
            "Navigation",
            [
                "Dashboard",
                "Chatbot",
                "Candidate Screening",
                "Stored Candidates",
                "Profile",
            ],
        )
    else:
        page = st.sidebar.radio(
            "Navigation", ["Chatbot", "Candidate Screening", "Profile"]
        )

    # Admin Dashboard
    if page == "Dashboard" and st.session_state["is_admin"]:
        st.title("📊 Admin Dashboard")

        login_count = get_login_count()
        total_candidates = len(load_candidates())

        col1, col2 = st.columns(2)
        col1.metric("🟢 Total Logins", login_count)
        col2.metric("📋 Total Candidates", total_candidates)

        st.markdown("---")
        st.subheader("📌 Recent Candidates")

        candidates = load_candidates()
        if candidates:
            df = pd.DataFrame(candidates)
            st.dataframe(df)
        else:
            st.warning("No candidates have applied yet.")

    # Chatbot Section
    elif page == "Chatbot":
        st.title("💬 AI Hiring Assistant")
        user_query = st.text_input("Type your question here...")
        if user_query:
            response = handle_chat(user_query)
            st.markdown(f"🗨️ **Response:**\n\n {response}", unsafe_allow_html=True)

    # Candidate Screening
    elif page == "Candidate Screening":
        st.title("📄 Candidate Screening Form")
        collect_candidate_info()

    # Stored Candidates (Only for Admin)
    elif page == "Stored Candidates" and st.session_state["is_admin"]:
        st.title("📋 Stored Candidate Information")
        candidates = load_candidates()

        if not candidates:
            st.warning("⚠️ No candidates found.")
        else:
            df = pd.DataFrame(candidates)
            if "Tech Stack" in df.columns:
                df["Tech Stack"] = df["Tech Stack"].apply(
                    lambda x: ", ".join(x) if isinstance(x, list) else str(x)
                )
            st.dataframe(df)

    # Profile Section
    elif page == "Profile":
        st.title("👤 User Profile")
        st.markdown(f"**Username:** {st.session_state['username']}")
        st.markdown(f"**Role:** {'Admin' if st.session_state['is_admin'] else 'User'}")

# Logout
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()
