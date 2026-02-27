import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

st.set_page_config(page_title="Vet Reminders",page_icon="🐾", layout="centered")
# 🔥 Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #111827;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔥 Centered Logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("logo.png", width=180)

st.title("🐾 PawsInn App Reminder")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "clinic_name" not in st.session_state:
    st.session_state.clinic_name = ""

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")

if uploaded_file:

    try:
        df_reminders = pd.read_excel(uploaded_file, sheet_name=0)
        df_users = pd.read_excel(uploaded_file, sheet_name=1)
    except Exception:
        st.error("Excel file must contain at least 2 sheets.")
        st.stop()

    # CLEAN COLUMN NAMES (Fix mobile bug)
    df_reminders.columns = df_reminders.columns.str.strip().str.lower()
    df_users.columns = df_users.columns.str.strip().str.lower()

    # ---------------- VALIDATE USER SHEET ----------------
    required_user_cols = {"username", "password", "expiry date", "clinic name"}

    if not required_user_cols.issubset(df_users.columns):
        st.error("Sheet2 format incorrect. Required columns: username, password, expiry date, clinic name")
        st.stop()

    # ---------------- LOGIN SECTION ----------------
    if not st.session_state.logged_in:

        st.subheader("🔐 Clinic Login")

        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):

            # Convert to string & strip spaces (extra safety)
            df_users["username"] = df_users["username"].astype(str).str.strip()
            df_users["password"] = df_users["password"].astype(str).str.strip()

            user_row = df_users[
                (df_users["username"] == username_input.strip()) &
                (df_users["password"] == password_input.strip())
            ]

            if user_row.empty:
                st.error("Invalid username or password")
            else:
                expiry_date = pd.to_datetime(
                    user_row.iloc[0]["expiry date"],
                    errors="coerce"
                ).date()

                clinic_name = user_row.iloc[0]["clinic name"]
                today = datetime.date.today()

                if pd.isna(expiry_date):
                    st.error("Invalid expiry date format in Sheet2.")
                elif today > expiry_date:
                    st.error("Subscription expired.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.clinic_name = clinic_name
                    st.rerun()

    # ---------------- AFTER LOGIN ----------------
    if st.session_state.logged_in:

        st.success(f"Welcome {st.session_state.clinic_name} ✅")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        # Validate reminder sheet columns
        required_reminder_cols = {"phone", "pet name", "owner name", "vaccine type", "due date"}

        if not required_reminder_cols.issubset(df_reminders.columns):
            st.error("Sheet1 format incorrect. Please check reminder columns.")
            st.stop()

        today = datetime.date.today()

        df_reminders["due date"] = pd.to_datetime(
            df_reminders["due date"],
            errors="coerce"
        ).dt.date

        df_today = df_reminders[df_reminders["due date"] == today]

        st.subheader("📋 Today's Reminders")

        if df_today.empty:
            st.info("No vaccinations due today.")
        else:
            for _, row in df_today.iterrows():

                phone = re.sub(r"\D", "", str(row["phone"]))
                if not phone.startswith("91"):
                    phone = "91" + phone

                pet = row["pet name"]
                owner = row["owner name"]
                vaccine = row["vaccine type"]

                message = f"Hi {owner}, this is a reminder that {pet} is due for a {vaccine} today."
                encoded_msg = urllib.parse.quote(message)

                wa_url = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}"

                with st.container(border=True):
                    st.write(f"*Pet:* {pet} | *Owner:* {owner}")
                    st.write(f"*Vaccine:* {vaccine} (Due Today)")
                    st.link_button(
                        f"Send to {pet}'s Owner",
                        wa_url,
                        use_container_width=True
                    )