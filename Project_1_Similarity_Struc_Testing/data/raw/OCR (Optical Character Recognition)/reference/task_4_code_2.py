

import requests



# Replace 'YOUR_SUBSCRIPTION_KEY' with your actual subscription key

subscription_key = 'YOUR_SUBSCRIPTION_KEY'

endpoint = 'https://<REGION>.api.cognitive.microsoft.com/'

ocr_url = endpoint + 'vision/v3.0/ocr'



image_url = 'URL_OF_ID_CARD_IMAGE'



headers = {

    'Ocp-Apim-Subscription-Key': subscription_key,

    'Content-Type': 'application/json',

}



params = {

    'language': 'en',

}



data = {'url': image_url}



response = requests.post(ocr_url, headers=headers, params=params, json=data)

response.raise_for_status()



analysis = response.json()

extracted_text = ''

for region in analysis['regions']:

    for line in region['lines']:

        for word in line['words']:

            extracted_text += word['text'] + ' '