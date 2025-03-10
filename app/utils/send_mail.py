import aiosmtplib
from email.message import EmailMessage
from typing import Optional
from pydantic import BaseModel

# Email Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "khalidmimm@gmail.com"
SENDER_PASSWORD = "cxuo yccn lzwn nxhq"  # Use environment variables for security!

class EmailSchema(BaseModel):
    receiver_email: str
    subject: str
    html_body: str

async def send_email(email_data: EmailSchema) -> Optional[bool]:
    """Send an email using an asynchronous SMTP client."""
    try:
        message = EmailMessage()
        message["From"] = f"AI Policing <{SENDER_EMAIL}>"
        message["To"] = email_data.receiver_email
        message["Subject"] = email_data.subject
        message.set_content(email_data.html_body, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SENDER_EMAIL,
            password=SENDER_PASSWORD,
            use_tls=True,
        )
        return True
    except Exception as e:
        return False
