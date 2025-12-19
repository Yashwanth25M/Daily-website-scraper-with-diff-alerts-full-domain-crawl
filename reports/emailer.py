import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# -------------------------------------------------
# Force-load .env from PROJECT ROOT
# Works for CLI, Scheduler, and Streamlit
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)


def send_email(html_content):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_email = os.getenv("FROM_EMAIL")
    to_email = os.getenv("TO_EMAIL")

    # -----------------------------
    # Validation
    # -----------------------------
    if not all([smtp_host, smtp_user, smtp_pass, from_email, to_email]):
        print("Email not configured. Missing SMTP environment variables.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Daily Website Change Report"
        msg["From"] = from_email
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully")
        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False
