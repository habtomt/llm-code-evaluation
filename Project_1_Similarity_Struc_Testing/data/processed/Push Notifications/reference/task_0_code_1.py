onesignal_client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_REST_API_KEY')

notification_contents ={

}

notification_headings ={

'en':'New Message Alert'

}

new_message_notification =onesignal .Notification (

contents =notification_contents ,headings =notification_headings ,

included_segments =['All']

)

onesignal_response =onesignal_client .send_notification (new_message_notification )

print (onesignal_response )