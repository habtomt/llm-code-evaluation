import onesignal

# Create an OneSignal client
client = onesignal.Client(app_id="<your_app_id>", rest_api_key="<your_rest_api_key>")

# Compose the urgent notification
notification = {
    "contents": {"en": "Security Alert: Potential security issue with your account. Please change your password immediately."},
    "included_segments": ["All"]
}

# Dispatch the urgent notification
response = client.send_notification(notification)
print(response)