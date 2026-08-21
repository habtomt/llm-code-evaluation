import onesignal

app_id ='YOUR_APP_ID'
api_key ='YOUR_API_KEY'

client =onesignal .Client (app_id =app_id ,rest_api_key =api_key )

notification_data ={
"contents":{"en":"A new version of the app is available with improvements and bug fixes!"},
"headings":{"en":"App Update Available"},
"included_segments":["All"]
}

response =client .send_notification (notification_data )

print (response )