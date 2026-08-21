import onesignal

client =onesignal .Client (app_id ="<your_app_id>",rest_api_key ="<your_rest_api_key>")

notification ={
"contents":{"en":"Security Alert: Potential security issue with your account. Please change your password immediately."},
"included_segments":["All"]
}

response =client .send_notification (notification )
print (response )