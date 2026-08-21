import onesignal

client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_REST_API_KEY')

notification =onesignal .Notification (

headings ={"en":"Hurry! Special Promotion Alert"},

included_segments =["All"]

)

response =client .send_notification (notification )

print (response )