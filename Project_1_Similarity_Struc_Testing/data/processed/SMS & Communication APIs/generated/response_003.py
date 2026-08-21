from twilio .rest import Client
import random
import string

account_sid ='your_account_sid'
auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

def send_sms (to_number ,message_body ):

    from_number ='+12345678901'

    try :
        message =client .messages .create (
        body =message_body ,
        from_ =from_number ,
        to =to_number
        )
        print (f"Message sent to {to_number}, Message SID: {message.sid}")
    except Exception as e :
        print (f"Failed to send message to {to_number}: {str(e)}")

def generate_password (length ):

    letters_and_digits =string .ascii_lowercase +string .digits
    password =''.join (random .choice (letters_and_digits )for _ in range (length ))
    return password

def notify_customer (inquiry_id ,customer_phone ,status ):

    message_body =(
    f "Update for your support inquiry
    "
    f"Current status: {status}. Thank you for your patience."
    )

    send_sms (customer_phone ,message_body )

    password_length =12
    password =generate_password (password_length )
    print (f"Generated password for customer: {password}")

def main ():

    customer_phone_number ='+1234567890'
    inquiry_id =1001
    status_update ="Resolved"

    notify_customer (inquiry_id ,customer_phone_number ,status_update )

if __name__ =="__main__":
    main ()