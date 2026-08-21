import onesignal

client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_REST_API_KEY')

message ="A new version of the app is available with improvements and bug fixes."

new_notification =onesignal .Notification (

contents ={"en":message },

)

new_notification .post_body ["included_segments"]=["Active Users"]

client .send_notification (new_notification )