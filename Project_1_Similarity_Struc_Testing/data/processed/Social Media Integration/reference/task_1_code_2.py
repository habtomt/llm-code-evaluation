`python

import requests

def get_facebook_feed (user_id ,access_token ):

    url =f"https://graph.facebook.com/v9.0/{user_id}/posts"

    params ={

    "access_token":access_token ,

    "fields":"id,message,created_time,full_picture,attachments{media_type,media_url}"

    }

    if response .status_code ==200 :

        return data ["data"]

    else :

        return None

user_id ="user123"

access_token ="your_access_token"

facebook_feed =get_facebook_feed (user_id ,access_token )

if facebook_feed :

    for post in facebook_feed :

        print (post )