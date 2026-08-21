import onesignal

onesignal_client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_REST_API_KEY')

notification_content ={
"headings":{"en":"New Message Alert"},
"contents":{"en":"You have received a new message from {{sender}}: {{message_snippet}}"}
}
sender ="John Doe"
message ="Hello! How are you doing?"

notification =onesignal .Notification (
contents =notification_content ,
included_segments =["ALL"],
data ={"sender":sender ,"message_snippet":message [:50 ]}
)

onesignal_client .send_notification (notification )