import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

st.set_page_config(page_title="Vet Reminders", page_icon="🐾", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#f97316;'>🐾 PawsInn App</h1>",
    unsafe_allow_html=True
)
st.subheader("Reminder Alert")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "clinic_name" not in st.session_state:
    st.session_state.clinic_name = ""

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")

if uploaded_file:

    excel_file = pd.ExcelFile(uploaded_file)

    # -------- Load Sheet1 (Required) --------
    df_reminders = pd.read_excel(excel_file, sheet_name=0)
    df_reminders.columns = df_reminders.columns.map(str)
    df_reminders.columns = df_reminders.columns.str.strip()

    # -------- Load Sheet2 (Optional & Safe) --------
    df_users = None
    login_enabled = False

    if len(excel_file.sheet_names) > 1:

        df_users = pd.read_excel(excel_file, sheet_name=1)

        if df_users.empty or df_users.shape[1] == 0:
            st.warning("Login detail not found!")
            login_enabled = False
        else:
            df_users.columns = df_users.columns.map(str)
            df_users.columns = df_users.columns.str.strip()

            required_user_cols = {"UserName", "Password", "Expiry", "ClinicName"}

            if required_user_cols.issubset(df_users.columns):
                login_enabled = True
            else:
                st.warning("Login detail not found! Login disabled.")
                login_enabled = False
    else:
        st.warning("Login detail not found!")
        login_enabled = False

    if not login_enabled:
        st.error("Login detail not found. App cannot proceed.")
        st.stop()

    # ---------------- LOGIN SECTION ----------------
    if login_enabled and not st.session_state.logged_in:

        st.subheader("🔐 Clinic Login")

        username_input = st.text_input("UserName")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):

            df_users["UserName"] = df_users["UserName"].astype(str).str.strip()
            df_users["Password"] = df_users["Password"].astype(str).str.strip()

            user_row = df_users[
                (df_users["UserName"] == username_input.strip()) &
                (df_users["Password"] == password_input.strip())
            ]

            if user_row.empty:
                st.error("Invalid username or password")
            else:
                expiry_date = pd.to_datetime(
                    user_row.iloc[0]["Expiry"],
                    errors="coerce"
                ).date()

                clinic_name = user_row.iloc[0]["ClinicName"]
                today = datetime.date.today()

                if pd.isna(expiry_date):
                    st.error("Invalid expiry date format.")
                elif today > expiry_date:
                    st.error("Subscription expired.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.clinic_name = clinic_name
                    st.rerun()

    # ---------------- AFTER LOGIN ----------------
    if st.session_state.logged_in:

        st.success(f"Welcome {st.session_state.clinic_name} ✅")

        if login_enabled:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

        required_reminder_cols = {"Contact No", "Pet Name", "Owner Name", "Description", "Due Date"}

        if not required_reminder_cols.issubset(df_reminders.columns):
            st.error("Sheet1 format incorrect.")
            st.stop()

        today = datetime.date.today()

        df_reminders["Due Date"] = pd.to_datetime(
            df_reminders["Due Date"],
            errors="coerce"
        ).dt.date

        df_today = df_reminders[df_reminders["Due Date"] == today]

        st.subheader("📋 Today's Reminders")

        if df_today.empty:
            st.info("No vaccinations due today.")
        else:
            for _, row in df_today.iterrows():

                phone = re.sub(r"\D", "", str(row["Contact No"]))
                if not phone.startswith("91"):
                    phone = "91" + phone

                pet = row["Pet Name"]
                owner = row["Owner Name"]
                vaccine = row["Description"]

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