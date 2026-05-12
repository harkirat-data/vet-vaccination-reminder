import streamlit as st
import pandas as pd
import urllib.parse
import datetime
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PawsInn – Vet Reminders",
    page_icon="🐾",
    layout="centered"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ========================= */
/* RESET */
/* ========================= */

*, *::before, *::after{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

/* ========================= */
/* REMOVE STREAMLIT HEADER */
/* ========================= */

header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer{
    display:none !important;
    visibility:hidden !important;
    height:0px !important;
}

/* ========================= */
/* BACKGROUND */
/* ========================= */

html,
body,
[data-testid="stAppViewContainer"]{
    background:#ffffff !important;
    font-family:'Nunito', sans-serif;
}

[data-testid="stAppViewContainer"]{
    background:
        radial-gradient(circle at top left,
        rgba(249,115,22,.08),
        transparent 30%),

        radial-gradient(circle at bottom right,
        rgba(249,115,22,.06),
        transparent 30%),

        #ffffff !important;
}

/* ========================= */
/* MAIN CONTAINER */
/* ========================= */

.block-container{
    max-width:700px !important;
    padding-top:0rem !important;
    padding-bottom:4rem !important;
    padding-left:1.5rem !important;
    padding-right:1.5rem !important;
    margin-top:-25px !important;
}

/* ========================= */
/* HERO */
/* ========================= */

.hero{
    text-align:center;
    padding:2rem 1rem 1.5rem;
}

.hero-paw{
    font-size:3rem;
}

.hero-title{
    font-family:'Fredoka One', cursive;
    font-size:3rem;

    background:linear-gradient(
        135deg,
        #fb923c 0%,
        #f97316 50%,
        #ea580c 100%
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-sub{
    color:#6b7280;
    font-size:.95rem;
    font-weight:700;
    letter-spacing:.15em;
    text-transform:uppercase;
    margin-top:.5rem;
}

.divider{
    width:60px;
    height:3px;

    background:linear-gradient(
        90deg,
        #f97316,
        #fb923c
    );

    border-radius:999px;
    margin:1rem auto 0;
}

/* ========================= */
/* CARD */
/* ========================= */

.card{
    background:#ffffff;
    border:1px solid rgba(249,115,22,.18);
    border-radius:20px;
    padding:2rem;
    box-shadow:0 4px 24px rgba(249,115,22,.10);
    margin-bottom:1.5rem;
}

.card-title{
    font-family:'Fredoka One', cursive;
    font-size:1.2rem;
    color:#fb923c;
    margin-bottom:1rem;
}

/* ========================= */
/* FILE UPLOADER */
/* ========================= */

[data-testid="stFileUploader"]{
    background:rgba(249,115,22,.04) !important;
    border:2px dashed rgba(249,115,22,.35) !important;
    border-radius:16px !important;
    padding:1rem !important;
}

/* ========================= */
/* INPUTS */
/* ========================= */

[data-testid="stTextInput"] input{
    background:#f9fafb !important;
    border:1.5px solid #e5e7eb !important;
    border-radius:12px !important;
    color:#111827 !important;
    padding:.75rem 1rem !important;
    font-size:.95rem !important;
}

[data-testid="stTextInput"] input:focus{
    border-color:#f97316 !important;
    box-shadow:0 0 0 3px rgba(249,115,22,.15) !important;
}

[data-testid="stTextInput"] label{
    color:#6b7280 !important;
    font-weight:700 !important;
}

/* ========================= */
/* BUTTONS */
/* ========================= */

[data-testid="stButton"] > button{
    background:linear-gradient(
        135deg,
        #f97316 0%,
        #ea580c 100%
    ) !important;

    color:white !important;
    border:none !important;
    border-radius:12px !important;
    padding:.75rem 1rem !important;
    width:100% !important;

    font-family:'Fredoka One', cursive !important;

    box-shadow:0 4px 18px rgba(249,115,22,.25) !important;
}

[data-testid="stButton"] > button:hover{
    transform:translateY(-2px);
}

/* ========================= */
/* LINK BUTTON */
/* ========================= */

[data-testid="stLinkButton"] a{
    background:linear-gradient(
        135deg,
        #22c55e 0%,
        #16a34a 100%
    ) !important;

    color:white !important;
    border-radius:12px !important;
    text-decoration:none !important;
    font-family:'Fredoka One', cursive !important;
}

/* ========================= */
/* BADGE */
/* ========================= */

.welcome-badge{
    display:inline-flex;
    align-items:center;
    gap:.5rem;

    background:rgba(34,197,94,.1);
    border:1px solid rgba(34,197,94,.3);

    color:#16a34a;

    padding:.5rem 1rem;
    border-radius:999px;

    font-family:'Fredoka One', cursive;
}

/* ========================= */
/* REMINDER CARD */
/* ========================= */

.reminder-card{
    background:#ffffff;
    border:1px solid rgba(249,115,22,.18);
    border-radius:18px;
    padding:1.2rem;
    margin-bottom:1rem;
    box-shadow:0 2px 12px rgba(249,115,22,.08);
}

.reminder-pet{
    font-family:'Fredoka One', cursive;
    color:#ea580c;
    font-size:1.1rem;
}

.reminder-owner{
    color:#4b5563;
    margin-top:.3rem;
}

.reminder-date{
    color:#6b7280;
    font-size:0.85rem;
    margin-top:0.3rem;
    font-weight:700;
}

.reminder-vaccine{
    display:inline-block;

    background:rgba(249,115,22,.10);
    color:#c2410c;

    padding:.3rem .8rem;
    border-radius:999px;

    font-size:.8rem;
    margin-top:.6rem;

    font-weight:700;
}

/* ========================= */
/* EMPTY STATE */
/* ========================= */

.empty-state{
    text-align:center;
    padding:2rem;
    color:#6b7280;
}

.empty-state .big{
    font-size:2.5rem;
}

/* ========================= */
/* HEADINGS */
/* ========================= */

h3{
    color:#1f2937 !important;
    font-family:'Fredoka One', cursive !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-paw">🐾</div>
    <div class="hero-title">PawsInn App</div>
    <div class="hero-sub">Reminder Alert</div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE INIT
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "clinic_name" not in st.session_state:
    st.session_state.clinic_name = ""

# Keep track of which list the user wants to view
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "due_today"

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# MAIN APP
# =========================================================

if uploaded_file:

    excel_file = pd.ExcelFile(uploaded_file)

    # =====================================================
    # SHEET 1
    # =====================================================

    df_reminders = pd.read_excel(excel_file, sheet_name=0)

    df_reminders.columns = (
        df_reminders.columns
        .map(str)
        .str.strip()
        .str.lower()
    )

    # =====================================================
    # SHEET 2 (LOGIN)
    # =====================================================

    login_enabled = False

    if len(excel_file.sheet_names) > 1:

        df_users = pd.read_excel(excel_file, sheet_name=1)

        df_users.columns = (
            df_users.columns
            .map(str)
            .str.strip()
        )

        required_login_cols = {
            "UserName",
            "Password",
            "Expiry",
            "ClinicName"
        }

        if required_login_cols.issubset(set(df_users.columns)):
            login_enabled = True

    if not login_enabled:
        st.error("❌ Login sheet not found.")
        st.stop()

    # =====================================================
    # LOGIN LOGIC
    # =====================================================

    if not st.session_state.logged_in:

        st.markdown(
            '<div class="card"><div class="card-title">🔐 Clinic Login</div>',
            unsafe_allow_html=True
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            df_users["UserName"] = (
                df_users["UserName"]
                .astype(str)
                .str.strip()
            )

            df_users["Password"] = (
                df_users["Password"]
                .astype(str)
                .str.strip()
            )

            user_row = df_users[
                (df_users["UserName"] == username.strip()) &
                (df_users["Password"] == password.strip())
            ]

            if user_row.empty:

                st.error("❌ Invalid username or password.")

            else:

                expiry = pd.to_datetime(
                    user_row.iloc[0]["Expiry"],
                    errors="coerce"
                ).date()

                today = datetime.date.today()

                if today > expiry:

                    st.error("🔒 Subscription expired.")

                else:

                    st.session_state.logged_in = True

                    st.session_state.clinic_name = (
                        user_row.iloc[0]["ClinicName"]
                    )

                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # DASHBOARD
    # =====================================================

    if st.session_state.logged_in:

        col1, col2 = st.columns([3,1])

        with col1:

            st.markdown(
                f'''
                <div class="welcome-badge">
                    ✅ {st.session_state.clinic_name}
                </div>
                ''',
                unsafe_allow_html=True
            )

        with col2:

            if st.button("Logout"):

                st.session_state.logged_in = False
                st.rerun()

        # =================================================
        # VALIDATION & DATE PARSING
        # =================================================

        required_cols = {
            "contact no",
            "pet name",
            "owner name",
            "description",
            "due date"
        }

        if not required_cols.issubset(set(df_reminders.columns)):
            st.error("❌ Sheet1 format incorrect.")
            st.stop()

        today = datetime.date.today()

        # dayfirst=True is crucial because your Excel has dates like 19/04/2026 (DD/MM/YYYY)
        df_reminders["due date"] = pd.to_datetime(
            df_reminders["due date"],
            dayfirst=True, 
            errors="coerce"
        ).dt.date

        # Generate DataFrames for the different views
        df_today = df_reminders[df_reminders["due date"] == today]
        df_upcoming = df_reminders[df_reminders["due date"] > today]

        total = len(df_reminders)
        due_today = len(df_today)
        upcoming = len(df_upcoming)

        # =================================================
        # STATS HTML CARDS
        # =================================================

        st.markdown(f"""
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:1rem;">
    <div style="background:rgba(249,115,22,.08); border:1px solid rgba(249,115,22,.18); border-radius:18px; padding:1rem; text-align:center;">
        <div style="font-family:'Fredoka One'; font-size:2rem; color:#f97316;">{total}</div>
        <div style="color:#6b7280; font-size:.8rem; font-weight:700; text-transform:uppercase;">Total Records</div>
    </div>
    <div style="background:rgba(239,68,68,.08); border:1px solid rgba(239,68,68,.18); border-radius:18px; padding:1rem; text-align:center;">
        <div style="font-family:'Fredoka One'; font-size:2rem; color:#ef4444;">{due_today}</div>
        <div style="color:#6b7280; font-size:.8rem; font-weight:700; text-transform:uppercase;">Due Today</div>
    </div>
    <div style="background:rgba(34,197,94,.08); border:1px solid rgba(34,197,94,.18); border-radius:18px; padding:1rem; text-align:center;">
        <div style="font-family:'Fredoka One'; font-size:2rem; color:#22c55e;">{upcoming}</div>
        <div style="color:#6b7280; font-size:.8rem; font-weight:700; text-transform:uppercase;">Upcoming</div>
    </div>
</div>
""", unsafe_allow_html=True)

        # =================================================
        # TAB BUTTONS (To switch views)
        # =================================================
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button("📂 View Total", use_container_width=True):
                st.session_state.view_mode = "total"
                
        with btn_col2:
            if st.button("🚨 View Due Today", use_container_width=True):
                st.session_state.view_mode = "due_today"
                
        with btn_col3:
            if st.button("📅 View Upcoming", use_container_width=True):
                st.session_state.view_mode = "upcoming"

        st.markdown("<hr style='border-top: 1px solid #e5e7eb; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # =================================================
        # LIST RENDERER
        # =================================================

        # Determine which dataframe and title to use based on the button clicked
        if st.session_state.view_mode == "total":
            df_active = df_reminders
            view_title = "📂 All Patient Records"
            empty_msg = "No patient records found in this file."
        elif st.session_state.view_mode == "upcoming":
            df_active = df_upcoming
            view_title = "📅 Upcoming Reminders"
            empty_msg = "No upcoming vaccinations scheduled."
        else:
            df_active = df_today
            view_title = "🚨 Today's Reminders"
            empty_msg = "No vaccinations due today. All paws are happy! 🎉"

        st.markdown(f"### {view_title}")

        if df_active.empty:

            st.markdown(f"""
<div class="empty-state">
    <div class="big">🐾</div>
    {empty_msg}
</div>
""", unsafe_allow_html=True)

        else:

            for _, row in df_active.iterrows():

                phone = re.sub(
                    r"\D",
                    "",
                    str(row["contact no"])
                )

                if not phone.startswith("91"):
                    phone = "91" + phone

                pet = row["pet name"]
                owner = row["owner name"]
                vaccine = row["description"]
                due_date_val = row["due date"]
                
                # Format Date for Display
                if pd.notnull(due_date_val):
                    date_str = due_date_val.strftime("%d %b %Y")
                else:
                    date_str = "Unknown Date"

                # Adjust the text message so it makes sense for future/past dates
                if st.session_state.view_mode == "due_today":
                    when_text = "today"
                else:
                    when_text = f"on {date_str}"

                message = (
                    f"Hi {owner}, "
                    f"{pet} is due for "
                    f"{vaccine} {when_text}."
                    f"If you need to reschedule or cancel, please call or text...{st.session_state.clinic_name} 🐾"
                )

                encoded_msg = urllib.parse.quote(message)

                wa_url = (
                    f"https://api.whatsapp.com/send?"
                    f"phone={phone}&text={encoded_msg}"
                )

                # PUSHED HARD LEFT TO AVOID CODE BLOCK BUG
                st.markdown(f"""
<div class="reminder-card">
    <div class="reminder-pet">
        🐶 {pet}
    </div>
    <div class="reminder-owner">
        Owner: {owner}
    </div>
    <div class="reminder-date">
        📅 Due: {date_str}
    </div>
    <div class="reminder-vaccine">
        💉 {vaccine}
    </div>
</div>
""", unsafe_allow_html=True)

                st.link_button(
                    f"📲 Send WhatsApp to {owner}",
                    wa_url,
                    use_container_width=True
                )