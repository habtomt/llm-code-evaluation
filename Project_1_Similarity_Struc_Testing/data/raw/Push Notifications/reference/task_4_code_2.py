

from onesignal_sdk.client import Client

client = Client(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY")



heading = {"en": "Limited Time Offer!"}

content = {"en": "Don't miss out on our exclusive promotional offer. Avail the discount now!"}





response = client.create_notification(notification_data)