import os
import smtplib
from email .mime .text import MIMEText
from email .mime .multipart import MIMEMultipart
from logging .handlers import SMTPHandler
import logging

logging .basicConfig (level =logging .INFO )
logger =logging .getLogger (__name__ )

def detect_security_issue (user_id ):

    return True

def send_email_notification (to_email ,subject ,message ):
    try :

        logger .info (f"Sending notification to {to_email}")
        with smtplib .SMTP ('smtp.gmail.com',587 )as server :
            server .starttls ()
            server .login (os .environ .get ('SMTP_USER'),os .environ .get ('SMTP_PASSWORD'))
            server .sendmail (os .environ .get ('SMTP_USER'),to_email ,message )
        logger .info ("Notification sent successfully!")
    except Exception as e :
        logger .error (f"Failed to send notification. Error: {e}")

def main ():

    SMTP_USER =os .environ .get ('SMTP_USER')
    SMTP_PASSWORD =os .environ .get ('SMTP_PASSWORD')
    USER_ID =os .environ .get ('USER_ID')
    USER_EMAIL =os .environ .get ('USER_EMAIL')

    if not all ([SMTP_USER ,SMTP_PASSWORD ,USER_ID ,USER_EMAIL ]):
        logger .error ("Missing environment variables")
        return

    if detect_security_issue (USER_ID ):

        notification_subject ="Urgent: Security Issue Detected, Password Change Required"
        notification_message =(
                    "Dear user ,

        "
        "We have detected a potential security issue with your account. "
                    "Please change your password immediately to secure your account .

        "
                    "Thank you ,
        "
        "Your Security Team"
        )

        send_email_notification (USER_EMAIL ,notification_subject ,notification_message )

if __name__ =="__main__":
    main ()