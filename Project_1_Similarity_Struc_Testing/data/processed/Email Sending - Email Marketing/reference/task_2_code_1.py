import sendgrid
import os
from sendgrid .helpers .mail import *
import datetime

sg =sendgrid .SendGridAPIClient (api_key =os .environ .get ('SENDGRID_API_KEY'))

def send_abandoned_cart_email (email ,products ):
    message =Mail (
    from_email ='noreply@example.com',
    to_emails =email ,
    subject ='Complete your purchase for personalized product recommendations!',
    html_content =f'''
        <p>Hello there,</p>
        <p>We noticed that you still have items in your shopping cart. Here are some personalized product recommendations based on your recent activity:</p>
        <ul>
            {"".join([f"<li>{product}</li>" for product in products])}
        </ul>
        <p>Don't miss out on these great finds! Click the link below to complete your purchase.</p>
        <p><a href="https://www.example.com/checkout">Complete your purchase</a></p>
        <p>Thank you for shopping with us!</p>
        '''
    )
    response =sg .send (message )
    print (response .status_code )
    print (response .body )
    print (response .headers )