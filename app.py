import streamlit as st
import pandas as pd
import urllib.parse

# Page config for better mobile view
st.set_page_config(page_title="Vet Reminders", layout="centered")

st.title("🐾 Vaccine Reminders")
st.write("Upload the Excel file generated from your CRM.")

# 1. Upload Logic
uploaded_file = st.file_uploader("Choose Excel File", type="xlsx")

if uploaded_file:
    # 2. Read the specific columns you mentioned
    df = pd.read_excel(uploaded_file)
    
    # Simple check to ensure columns exist (adjust names to match your VB6 export)
    expected_cols = ['phone', 'pet name', 'owner name', 'vaccine type', 'due date']
    
    st.subheader("Today's Reminders")
    
    for index, row in df.iterrows():
        # Data Extraction
        phone = str(row['phone']).replace(" ", "").replace("+", "")
        pet = row['pet name']
        owner = row['owner name']
        vaccine = row['vaccine type']
        due = row['due date']

        # 3. Create WhatsApp URL
        message = f"Hi {owner}, this is a reminder that {pet} is due for a {vaccine} on {due}."
        encoded_msg = urllib.parse.quote(message)
        wa_url = f"https://wa.me/{phone}?text={encoded_msg}"

        # 4. Mobile UI: One clean card per reminder
        with st.container(border=True):
            st.write(f"*Pet:* {pet} | *Owner:* {owner}")
            st.write(f"*Vaccine:* {vaccine} (Due: {due})")
            
            # The Magic Button: Opens WhatsApp Mobile App
            st.link_button(f"Send to {pet}'s Owner", wa_url, use_container_width=True)