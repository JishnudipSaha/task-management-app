from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from src.utils.settings import settings





conf = ConnectionConfig(
    MAIL_USERNAME = "jishnudip.saha.2004@gmail.com",
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = "jishnudip.saha.2004@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Jishnu's task-management app",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(emails: List[str]):
    body = 'Hi there, thanks for the registration, and thanks for the registration !!!'
    html = f"<p>{body}</p> "

    message = MessageSchema(
        subject="Registration Confirmed",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}