`python

import requests



def share_to_facebook(access_token, content):

    url = "https://graph.facebook.com/me/feed"

        "message": content,

        "access_token": access_token

    }

    return response.json()



# Example usage

access_token = "user_access_token"

content = "Check out this amazing content!"

response = share_to_facebook(access_token, content)

print(response)