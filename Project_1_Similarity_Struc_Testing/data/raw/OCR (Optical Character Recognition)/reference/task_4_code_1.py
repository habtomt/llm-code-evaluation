

import requests



subscription_key = 'YOUR_SUBSCRIPTION_KEY'

endpoint = 'https://YOUR_AZURE_REGION_NAME.api.cognitive.microsoft.com'



image_url = 'URL_TO_ID_CARD_IMAGE'



headers = {

    'Ocp-Apim-Subscription-Key': subscription_key,

    'Content-Type': 'application/json',

}



params = {

    'language': 'en',

    'detectOrientation': 'true',

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



print(extracted_text)