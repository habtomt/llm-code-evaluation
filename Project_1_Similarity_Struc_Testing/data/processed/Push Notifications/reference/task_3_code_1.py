import onesignal

client =onesignal .Client (app_id ='YOUR_APP_ID',rest_api_key ='YOUR_REST_API_KEY')

notification ={

'included_segments':['All'],

'priority':10

}

response =client .create_notification (notification )

print (response )