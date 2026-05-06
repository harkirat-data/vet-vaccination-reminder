import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

st.set_page_config(page_title="PawsInn – Vet Reminders", page_icon="🐾", layout="centered")

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0f1117 !important;
    font-family: 'Nunito', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(249,115,22,.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(234,88,12,.12) 0%, transparent 55%),
        #0f1117 !important;
    min-height: 100vh;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ── Main container ── */
.block-container {
    max-width: 680px !important;
    padding: 2.5rem 1.5rem 4rem !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 1.6rem;
    position: relative;
}
.hero-paw {
    font-size: 3.2rem;
    display: block;
    animation: bounce 2.4s ease-in-out infinite;
}
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}
.hero-title {
    font-family: 'Fredoka One', cursive;
    font-size: 3rem;
    letter-spacing: .03em;
    background: linear-gradient(135deg, #fb923c 0%, #f97316 50%, #ea580c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-top: .3rem;
}
.hero-sub {
    color: #9ca3af;
    font-size: .95rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-top: .5rem;
}
.divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #f97316, #fb923c);
    border-radius: 999px;
    margin: 1rem auto 0;
}

/* ── Card wrapper ── */
.card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 20px;
    padding: 2rem 2rem 1.6rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 40px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.06);
    margin-bottom: 1.4rem;
}
.card-title {
    font-family: 'Fredoka One', cursive;
    font-size: 1.25rem;
    color: #fb923c;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}

/* ── Upload widget ── */
[data-testid="stFileUploader"] {
    background: rgba(249,115,22,.06) !important;
    border: 2px dashed rgba(249,115,22,.35) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    transition: border-color .25s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(249,115,22,.7) !important;
}
[data-testid="stFileUploader"] label {
    color: #d1d5db !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.06) !important;
    border: 1.5px solid rgba(255,255,255,.12) !important;
    border-radius: 12px !important;
    color: #f9fafb !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: .97rem !important;
    padding: .7rem 1rem !important;
    transition: border-color .2s, box-shadow .2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,.2) !important;
    outline: none !important;
}
[data-testid="stTextInput"] label {
    color: #9ca3af !important;
    font-weight: 700 !important;
    font-size: .82rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.05rem !important;
    letter-spacing: .04em !important;
    padding: .65rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: transform .15s, box-shadow .15s, opacity .15s !important;
    box-shadow: 0 4px 18px rgba(249,115,22,.4) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(249,115,22,.55) !important;
    opacity: .92 !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* logout button – ghost style */
[data-testid="stButton"]:has(button[kind="secondary"]) > button,
.logout-btn [data-testid="stButton"] > button {
    background: transparent !important;
    border: 1.5px solid rgba(249,115,22,.45) !important;
    color: #fb923c !important;
    box-shadow: none !important;
    font-size: .88rem !important;
    padding: .4rem 1.2rem !important;
    width: auto !important;
}

/* ── Link button (WhatsApp) ── */
[data-testid="stLinkButton"] a {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: .5rem !important;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    color: #fff !important;
    border-radius: 12px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1rem !important;
    padding: .6rem 1rem !important;
    text-decoration: none !important;
    box-shadow: 0 4px 16px rgba(34,197,94,.35) !important;
    transition: transform .15s, box-shadow .15s !important;
}
[data-testid="stLinkButton"] a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(34,197,94,.5) !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
}

/* ── Section headings ── */
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Fredoka One', cursive;
    color: #f9fafb;
    font-size: 1.35rem;
    margin: .4rem 0 1rem;
}

/* ── Reminder card ── */
.reminder-card {
    background: rgba(249,115,22,.07);
    border: 1px solid rgba(249,115,22,.2);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: transform .18s, box-shadow .18s;
    position: relative;
    overflow: hidden;
}
.reminder-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #fb923c, #f97316);
    border-radius: 4px 0 0 4px;
}
.reminder-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(249,115,22,.18);
}
.reminder-pet { font-family:'Fredoka One',cursive; font-size:1.15rem; color:#fb923c; }
.reminder-owner { color:#d1d5db; font-size:.92rem; font-weight:600; margin:.18rem 0 .5rem; }
.reminder-vaccine {
    display: inline-block;
    background: rgba(249,115,22,.15);
    color: #fed7aa;
    font-size: .8rem;
    font-weight: 700;
    letter-spacing: .07em;
    text-transform: uppercase;
    padding: .22rem .75rem;
    border-radius: 999px;
    margin-bottom: .85rem;
}
.welcome-badge {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    background: rgba(34,197,94,.12);
    border: 1px solid rgba(34,197,94,.3);
    color: #4ade80;
    font-family: 'Fredoka One', cursive;
    font-size: 1rem;
    padding: .5rem 1.1rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #6b7280;
    font-size: .95rem;
    font-weight: 600;
}
.empty-state .big { font-size: 2.5rem; margin-bottom: .5rem; }
</style>
""", unsafe_allow_html=True)

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-paw">🐾</span>
    <div class="hero-title">PawsInn App</div>
    <div class="hero-sub">Vaccine Reminder System</div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "clinic_name" not in st.session_state:
    st.session_state.clinic_name = ""

# ─── FILE UPLOAD ───────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📂 Upload Patient Data</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drop your Excel file here", type="xlsx", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)

    # Sheet1 – reminders
    df_reminders = pd.read_excel(excel_file, sheet_name=0)
    df_reminders.columns = df_reminders.columns.map(str).str.strip().str.lower()

    # Sheet2 – users
    df_users = None
    login_enabled = False

    if len(excel_file.sheet_names) > 1:
        df_users = pd.read_excel(excel_file, sheet_name=1)
        if not df_users.empty and df_users.shape[1] > 0:
            df_users.columns = df_users.columns.map(str).str.strip()  # keep original case for login cols
            required_user_cols = {"UserName", "Password", "Expiry", "ClinicName"}
            if required_user_cols.issubset(set(df_users.columns)):
                login_enabled = True
            else:
                st.warning("⚠️ Login sheet columns don't match expected format.")
        else:
            st.warning("⚠️ Login sheet is empty.")
    else:
        st.warning("⚠️ No login sheet found.")

    if not login_enabled:
        st.error("🚫 Login details not found. App cannot proceed.")
        st.stop()

    # ─── LOGIN ────────────────────────────────────────────────────────────────
    if not st.session_state.logged_in:
        st.markdown('<div class="card"><div class="card-title">🔐 Clinic Login</div>', unsafe_allow_html=True)
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")

        if st.button("Login →"):
            df_users["UserName"] = df_users["UserName"].astype(str).str.strip()
            df_users["Password"] = df_users["Password"].astype(str).str.strip()

            user_row = df_users[
                (df_users["UserName"] == username_input.strip()) &
                (df_users["Password"] == password_input.strip())
            ]

            if user_row.empty:
                st.error("❌ Invalid username or password.")
            else:
                expiry_date = pd.to_datetime(user_row.iloc[0]["Expiry"], errors="coerce").date()
                clinic_name = user_row.iloc[0]["ClinicName"]
                today = datetime.date.today()

                if pd.isna(expiry_date):
                    st.error("❌ Invalid expiry date format.")
                elif today > expiry_date:
                    st.error("🔒 Subscription expired. Please renew.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.clinic_name = clinic_name
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ─── DASHBOARD ────────────────────────────────────────────────────────────
    if st.session_state.logged_in:

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f'<div class="welcome-badge">✅ {st.session_state.clinic_name}</div>',
                unsafe_allow_html=True
            )
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

        # validate sheet1
        required_reminder_cols = {"contact no", "pet name", "owner name", "description", "due date"}
        if not required_reminder_cols.issubset(set(df_reminders.columns)):
            st.error("⚠️ Sheet1 column format incorrect. Expected: Contact No, Pet Name, Owner Name, Description, Due Date")
            st.stop()

        today = datetime.date.today()
        df_reminders["due date"] = pd.to_datetime(df_reminders["due date"], errors="coerce").dt.date
        df_today = df_reminders[df_reminders["due date"] == today]

        # stats row
        total = len(df_reminders)
        due_today = len(df_today)
        upcoming = len(df_reminders[df_reminders["due date"] > today])

        st.markdown(f"""
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:1.4rem;">
            <div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:16px;padding:1rem;text-align:center;">
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#fb923c;">{total}</div>
                <div style="color:#9ca3af;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;">Total Records</div>
            </div>
            <div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);border-radius:16px;padding:1rem;text-align:center;">
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#f87171;">{due_today}</div>
                <div style="color:#9ca3af;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;">Due Today</div>
            </div>
            <div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:16px;padding:1rem;text-align:center;">
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#4ade80;">{upcoming}</div>
                <div style="color:#9ca3af;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;">Upcoming</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Today's Reminders")

        if df_today.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="big">🎉</div>
                No vaccinations due today. All paws are happy!
            </div>
            """, unsafe_allow_html=True)
        else:
            for _, row in df_today.iterrows():
                phone = re.sub(r"\D", "", str(row["contact no"]))
                if not phone.startswith("91"):
                    phone = "91" + phone

                pet     = row["pet name"]
                owner   = row["owner name"]
                vaccine = row["description"]

                message     = f"Hi {owner}, this is a friendly reminder that *{pet}* is due for *{vaccine}* today. Please visit us at your earliest convenience. 🐾"
                encoded_msg = urllib.parse.quote(message)
                wa_url      = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}"

                st.markdown(f"""
                <div class="reminder-card">
                    <div class="reminder-pet">🐶 {pet}</div>
                    <div class="reminder-owner">Owner: {owner} &nbsp;·&nbsp; 📞 {phone[2:]}</div>
                    <span class="reminder-vaccine">💉 {vaccine}</span>
                </div>
                """, unsafe_allow_html=True)

                st.link_button(f"📲 Send WhatsApp to {owner}", wa_url, use_container_width=True)