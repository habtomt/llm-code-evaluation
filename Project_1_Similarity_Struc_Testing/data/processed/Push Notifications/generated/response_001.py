import smtplib
from email .mime .text import MIMEText
from email .mime .multipart import MIMEMultipart
from email .mime .base import MIMEBase
from email import encoders
import os

smtp_server ='smtp.example.com'
smtp_port =587
smtp_user ='your_email@example.com'
smtp_password ='your_password'

recipients =['user1@example.com','user2@example.com']

subject ='New Version of Our App is Now Available!'
body ='''\
Hello,

We're excited to announce that a new version of our app has been released. This update includes several improvements and bug fixes to enhance your experience.

Key updates:
- Performance improvements
- New features added
- Bug fixes

We hope you enjoy the updates. Please let us know if you have any feedback.

Best regards,
Your App Team
'''

def send_emails (smtp_server ,smtp_port ,smtp_user ,smtp_password ,recipients ,subject ,body ):

    server =smtplib .SMTP (smtp_server ,smtp_port )
    server .starttls ()
    server .login (smtp_user ,smtp_password )

    msg =MIMEMultipart ()
    msg ['From']=smtp_user
    msg ['Subject']=subject
    msg .attach (MIMEText (body ,'plain'))

    filename ='changelog.txt'
    if os .path .exists (filename ):
        attachment =open (filename ,'rb')
        part =MIMEBase ('application','octet-stream')
        part .set_payload (attachment .read ())
        encoders .encode_base64 (part )
        part .add_header ('Content-Disposition',f'attachment; filename= {filename}')
        msg .attach (part )

    for recipient in recipients :
        msg ['To']=recipient
        try :

            server .sendmail (smtp_user ,recipient ,msg .as_string ())
            print (f'Email sent to {recipient}')
        except Exception as e :
            print (f'Failed to send email to {recipient}: {e}')

    server .quit ()

send_emails (smtp_server ,smtp_port ,smtp_user ,smtp_password ,recipients ,subject ,body )