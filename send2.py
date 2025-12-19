import pandas as pd
import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# ZOHO SMTP CONFIG
# =========================
SMTP_SERVER = "smtp.zoho.in"      # use smtp.zoho.com if not India
SMTP_PORT = 587
ZOHO_EMAIL = "arjun@maileasy.co"
ZOHO_APP_PASSWORD = st.secrets["APP_PASS"]

# =========================
# FILE CONFIG
# =========================
CSV_FILE = "apollo_outreach_emails.csv"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Zoho Email Sender", layout="wide")
st.title("📧 Zoho CSV Email Sender")

# =========================
# LOAD CSV
# =========================
@st.cache_data
def load_csv():
    return pd.read_csv(CSV_FILE, encoding="latin1")

df = load_csv()

# =========================
# INIT SESSION STATE
# =========================
if "sent_rows" not in st.session_state:
    st.session_state.sent_rows = set()

# =========================
# EMAIL FUNCTION
# =========================
def send_email(to_email, first_name, email_body):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(ZOHO_EMAIL, ZOHO_APP_PASSWORD)

    subject = f"Quick note, {first_name}"

    msg = MIMEMultipart()
    msg["From"] = ZOHO_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_body, "plain"))

    server.send_message(msg)
    server.quit()

# =========================
# TABLE VIEW
# =========================
st.write("### Leads")
for idx, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 2.5, 3, 5, 1.2])

    with col1:
        st.write(row.get("First Name", ""))

    with col2:
        st.write(row.get("Last Name", ""))

    with col3:
        st.write(row.get("Email", ""))

    with col4:
        st.write(row.get("Company Name", ""))

    with col5:
        st.text_area(
            label="",
            value=str(row.get("Generated Email", "")),
            height=160,
            key=f"email_{idx}"
        )

    with col6:
        if idx in st.session_state.sent_rows:
            st.success("Sent")
        else:
            if st.button("Send", key=f"send_{idx}"):
                try:
                    send_email(
                        to_email=str(row["Email"]).strip(),
                        first_name=str(row["First Name"]).strip(),
                        email_body=str(row["Generated Email"]).strip()
                    )
                    st.session_state.sent_rows.add(idx)
                    st.success("Sent")
                except Exception as e:
                    st.error("Failed")
