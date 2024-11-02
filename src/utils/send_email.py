import aiosmtplib
from email.message import EmailMessage
from config.config import email_settings


async def send_password_email(to_email: str, password: str) -> None:
    EMAIL_ADDRESS = email_settings.EMAIL_SENDER  # noqa: N806
    EMAIL_PASSWORD = email_settings.EMAIL_PASSWORD  # noqa: N806
    EMAIL_PORT = email_settings.EMAIL_PORT  # noqa: N806

    msg = EmailMessage()
    msg["Subject"] = "Your Account Password"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    html_content = f"""
    <html>
        <body>
            <h2>Hello,</h2>
            <p>Your account has been created.</p>
            <p><strong>Your password is:</strong> {password}</p>
            <p>You can change it after logging in</p>
            <p>Best regards,<br>Your Company</p>
        </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")
    smtp = aiosmtplib.SMTP(
        hostname="smtp.gmail.com", port=EMAIL_PORT
    )  # Initialize with hostname and port
    try:
        await smtp.connect()  # Connect to the server
        await smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        await smtp.send_message(msg)
        print("Password sent successfully!")  # noqa: T201
    except Exception as e:
        print(f"Error sending email: {e}")  # noqa: T201
    finally:
        if smtp.is_connected:
            await smtp.quit()
