import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

# Page config for better mobile view
st.set_page_config(page_title="Vet Reminders", layout="centered")

st.title("🐾 Vaccine Reminders")
st.write("Upload the Excel file generated from your CRM.")

# 1. Upload Logic
uploaded_file = st.file_uploader("Choose Excel File", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    expected_cols = ['phone', 'pet name', 'owner name', 'vaccine type', 'due date']
    if not all(col in df.columns for col in expected_cols):
        st.error("Excel file format is incorrect. Please check column names.")
        st.stop()

    st.subheader("Today's Reminders")

    # Convert due date column properly
    df['due date'] = pd.to_datetime(df['due date'], errors='coerce').dt.date

    today = datetime.date.today()

    # Filter only today's reminders
    df_today = df[df['due date'] == today]

    if df_today.empty:
        st.info("No vaccinations due today.")
    else:
        for index, row in df_today.iterrows():

            # Clean phone number
            phone = re.sub(r'\D', '', str(row['phone']))
            if not phone.startswith("91"):
                phone = "91" + phone

            pet = row['pet name']
            owner = row['owner name']
            vaccine = row['vaccine type']

            # Create WhatsApp message
            message = f"Hi {owner}, this is a reminder that {pet} is due for a {vaccine} today."
            encoded_msg = urllib.parse.quote(message)

            wa_url = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}"

            # UI Card
            with st.container(border=True):
                st.write(f"*Pet:* {pet} | *Owner:* {owner}")
                st.write(f"*Vaccine:* {vaccine} (Due Today)")
                st.link_button(
                    f"Send to {pet}'s Owner",
                    wa_url,
                    use_container_width=True
                )   