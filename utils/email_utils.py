import smtplib
from email.mime.text import MIMEText
from jose import jwt
from datetime import datetime, timedelta
from config import SMTP_EMAIL, SMTP_PASSWORD, VERIFY_TOKEN_SECRET, VERIFY_TOKEN_EXPIRE_MINUTES, ALGORITHM, BASE_URL

def create_email_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=VERIFY_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, VERIFY_TOKEN_SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, VERIFY_TOKEN_SECRET, algorithms=[ALGORITHM])
        return payload["sub"]
    except Exception:
        return None

def send_verification_email(to_email: str, token: str):
    verify_link = f"{BASE_URL}/verify-email?token={token}"

    msg = MIMEText(f"Click this link to verify your email: \n\n{verify_link}")
    msg["Subject"] = "Verify your email"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)       
