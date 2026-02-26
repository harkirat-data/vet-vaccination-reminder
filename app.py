import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

st.set_page_config(page_title="Vet Reminders", layout="centered")

st.title("🐾 PawsInn App Reminder")

# Session state initialize
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")

if uploaded_file:

    df_reminders = pd.read_excel(uploaded_file, sheet_name=0)
    df_users = pd.read_excel(uploaded_file, sheet_name=1)

    # ---------- LOGIN SECTION ----------
    if not st.session_state.logged_in:

        st.subheader("🔐 Clinic Login")

        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):

            user_row = df_users[
                (df_users['username'] == username_input) &
                (df_users['password'] == password_input)
            ]

            if user_row.empty:
                st.error("Invalid username or password")
            else:
                expiry_date = pd.to_datetime(
                    user_row.iloc[0]['expiry date']
                ).date()

                clinic_name = user_row.iloc[0]['clinic name']
                today = datetime.date.today()

                if today > expiry_date:
                    st.error("Subscription expired.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.clinic_name = clinic_name
                    st.rerun()

    # ---------- AFTER LOGIN ----------
    if st.session_state.logged_in:

        st.success(f"Welcome {st.session_state.clinic_name} ✅")

        # Optional Logout Button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        today = datetime.date.today()

        df_reminders['due date'] = pd.to_datetime(
            df_reminders['due date'],
            errors='coerce'
        ).dt.date

        df_today = df_reminders[df_reminders['due date'] == today]

        st.subheader("📋 Today's Reminders")

        if df_today.empty:
            st.info("No vaccinations due today.")
        else:
            for index, row in df_today.iterrows():

                phone = re.sub(r'\D', '', str(row['phone']))
                if not phone.startswith("91"):
                    phone = "91" + phone

                pet = row['pet name']
                owner = row['owner name']
                vaccine = row['vaccine type']

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