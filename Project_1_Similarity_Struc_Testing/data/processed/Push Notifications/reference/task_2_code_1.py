import onesignal

client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_API_KEY')

notification =onesignal .Notification (
contents ={"en":"Upcoming Event Reminder: Don't miss the event on [EVENT_DATE] at [EVENT_TIME]."},
include_player_ids =["USER_PLAYER_ID_1","USER_PLAYER_ID_2"]
)

response =client .send_notification (notification )

print (response )