from flask import Flask ,session ,jsonify ,request
from datetime import datetime ,timedelta
import smtplib
from email .message import EmailMessage
import threading
import time

app =Flask (__name__ )
app .secret_key ='your_secret_key'

user_cart_info ={}
user_emails ={
'user_id_1':'user1@example.com',

}

def get_recommended_products (user_id ):

    return ["Product A","Product B"]

@app .route ("/add_to_cart",methods =["POST"])
def add_to_cart ():
    user_id =request .json .get ('user_id')
    product_id =request .json .get ('product_id')
    session .modified =True
    if user_id not in user_cart_info :
        user_cart_info [user_id ]=[]
    user_cart_info [user_id ].append ({
    "product_id":product_id ,
    "timestamp":datetime .utcnow ()
    })
    return jsonify ({"message":"Product added to cart"}),200

def check_and_send_abandoned_cart_emails ():
    while True :
        now =datetime .utcnow ()
        for user_id ,cart_items in user_cart_info .items ():

            abandoned_items =[item for item in cart_items if now -item ['timestamp']>timedelta (hours =24 )]
            if abandoned_items :
                email_address =user_emails .get (user_id ,None )
                if email_address :

                    recommendations =get_recommended_products (user_id )

                    send_abandoned_cart_email (email_address ,recommendations )
        time .sleep (3600 )

def send_abandoned_cart_email (email_address ,recommendations ):
    try :
        msg =EmailMessage ()
        msg .set_content (f"Hey, we noticed you left some items in your cart! You might also like: {', '.join(recommendations)}")
        msg ['Subject']="Complete Your Purchase!"
        msg ['From']="yourshop@example.com"
        msg ['To']=email_address

        with smtplib .SMTP ('localhost')as s :
            s .send_message (msg )
    except Exception as e :
        print (f"Error sending email: {e}")

thread =threading .Thread (target =check_and_send_abandoned_cart_emails )
thread .daemon =True
thread .start ()

if __name__ =="__main__":
    app .run (debug =True )