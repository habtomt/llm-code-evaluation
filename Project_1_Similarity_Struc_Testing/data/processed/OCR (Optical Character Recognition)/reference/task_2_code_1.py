import requests

subscription_key ='YOUR_SUBSCRIPTION_KEY'

ocr_url =f"{endpoint}/vision/v3.1/ocr"

image_url ='URL_OF_IMAGE_WITH_LICENSE_PLATE'

headers ={

'Ocp-Apim-Subscription-Key':subscription_key ,

'Content-Type':'application/json'

}

params ={

'language':'unk',

'detectOrientation':'true'

}

response =requests .post (ocr_url ,headers =headers ,params =params ,json ={"url":image_url })

ocr_result =response .json ()

for region in ocr_result ['regions']:

    for line in region ['lines']:

        print (license_plate_text )