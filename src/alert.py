import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_alert(subject, message, recipient):
    """
    Send an email alert using Yahoo's SMTP server.

    Args:
    - subject (str): Subject of the email.
    - message (str): Body of the email.
    - recipient (str): Recipient email address.
    """
    # Retrieve email credentials from environment variables
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_host = os.getenv("EMAIL_HOST")
    email_port = os.getenv("EMAIL_PORT")
    email_use_ssl = os.getenv("EMAIL_USE_SSL") == 'True'

    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish an SSL connection to the email server
        if email_use_ssl:
            server = smtplib.SMTP_SSL(email_host, email_port)
        else:
            server = smtplib.SMTP(email_host, email_port)
            server.starttls()  # Start TLS if SSL is not used

        # Log in to the email server
        server.login(email_username, email_password)

        # Send the email
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        print(f"Alert email sent to {recipient}.")

    except Exception as e:
        print(f"Failed to send alert email: {str(e)}")

    finally:
        server.quit()  # Always close the server connection
