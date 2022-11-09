import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv 
from pathlib import Path

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)


# Define email sender and receiver
email_sender = os.getenv("EMAIL")
email_password = os.getenv("PASSWORD")  

def send_email(subject, email_receiver, name, due_date, invoice_no, amount):
    
    # Set the subject and body of the email
    em = EmailMessage()
    em["From"] = formataddr(("Email Testing.", f"{email_sender}"))
    em['To'] = email_receiver
    em['Subject'] = subject
    em["BCC"] = email_sender
    
    em.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        I just wanted to drop you a quick note to remind you that {amount} USD in respect of our invoice {invoice_no} is due for payment on {due_date}.
        I would be really grateful if you could confirm that everything is on track for payment.
        Best regards
        YOUR NAME
        """
    )
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    em.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hi {name},</p>
        <p>I hope you are well.</p>
        <p>I just wanted to drop you a quick note to remind you that <strong>{amount} USD</strong> in respect of our invoice {invoice_no} is due for payment on <strong>{due_date}</strong>.</p>
        <p>I would be really grateful if you could confirm that everything is on track for payment.</p>
        <p>Best regards</p>
        <p>YOUR NAME</p>
      </body>
    </html>
    """,
        subtype="html",
    )
    
    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        
if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Mart Skuthi",
        email_receiver = 'martskuthi@gmail.com',
        due_date="11, Aug 2022",
        invoice_no="INV-21-12-009",
        amount="5",
    )