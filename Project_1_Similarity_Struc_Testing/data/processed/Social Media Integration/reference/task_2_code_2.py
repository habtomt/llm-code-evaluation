`python

import requests

def share_content_to_facebook(access_token, content):

    api_url = "https://graph.facebook.com/me/feed"

    headers = {

        "Authorization": f"Bearer {access_token}",

    }

    data = {

        "message": content

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:

        return "Content shared successfully on Facebook"

    else:

        return "Failed to share content on Facebook"

access_token = "your_user_access_token"

content = "Check out this amazing content!"

result = share_content_to_facebook(access_token, content)

print(result)