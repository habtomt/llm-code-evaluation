

import onesignal





client = onesignal.Client(app_id, api_key)



notification = {

    "contents": {"en": "Don't forget about the upcoming event!"},

    "headings": {"en": "Event Reminder"},

    "url": "https://your-website.com/event-details",

    "send_after": "2022-12-31 12:00:00 GMT-0700",

    "data": {"eventId": "EVENT_ID"}

}



client.send_notification(notification)