import smtplib
from email .mime .multipart import MIMEMultipart
from email .mime .text import MIMEText
from datetime import datetime
import pytz
import os
import time

subscribers =[
{"name":"Alice","email":"alice@example.com","timezone":"America/New_York"},
{"name":"Bob","email":"bob@example.com","timezone":"Europe/London"},

]

def send_email (subscriber ):
    name =subscriber ["name"]
    email =subscriber ["email"]
    timezone =subscriber ["timezone"]

    local_tz =pytz .timezone (timezone )
    local_time =datetime .now (local_tz )

    if 8 <=local_time .hour <=20 :

        from_addr =os .environ .get ('FROM_EMAIL')
        to_addr =email
        msg =MIMEMultipart ()
        msg ['From']=from_addr
        msg ['To']=to_addr
        msg ['Subject']="Special Offer Just for You!"

        body =f"""
        Hi {name},

        We are excited to offer you an exclusive discount!

        Best Regards,
        Your Company
        """

        msg .attach (MIMEText (body ,'plain'))

        try :
            server =smtplib .SMTP (os .environ .get ('SMTP_SERVER'),int (os .environ .get ('SMTP_PORT')))
            server .starttls ()
            server .login (os .environ .get ('FROM_EMAIL'),os .environ .get ('EMAIL_PASSWORD'))
            server .send_message (msg )
            server .quit ()
            print (f"Email sent to {name} at {email}")
        except Exception as e :
            print (f"Failed to send email to {name}: {str(e)}")

for subscriber in subscribers :
    send_email (subscriber )
    time .sleep (60 )