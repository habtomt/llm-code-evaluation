import os

from sendgrid import SendGridAPIClient

from sendgrid .helpers .mail import Mail ,Email ,Personalization ,Content

sg_api_key =os .environ .get ('SENDGRID_API_KEY')

sg_client =SendGridAPIClient (sg_api_key )

def send_promotional_email (email_list ,customer_data ):

    for email in email_list :

        message =Mail (

        from_email ='your@email.com',

        to_emails =email ,

        subject ='Your Subject',

        html_content ='<strong>Your HTML message here</strong>'

        )

        personalization =Personalization ()

        personalization .add_to (Email (email ))

        personalization .add_dynamic_template_data (customer_data [email ])

        message .add_personalization (personalization )

        print (response .body )