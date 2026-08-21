import requests

import json

subscription_key ='YOUR_SUBSCRIPTION_KEY'

endpoint ='YOUR_ENDPOINT'

ocr_url =endpoint +'/vision/v3.1/ocr'

image_path ='PATH_TO_IMAGE_FILE'

headers ={

'Ocp-Apim-Subscription-Key':subscription_key ,

'Content-Type':'application/octet-stream'

}

with open (image_path ,'rb')as image_file :

    image_data =image_file .read ()

response =requests .post (ocr_url ,headers =headers ,data =image_data )

response .raise_for_status ()

analysis =response .json ()

regions =analysis ['regions']

for region in regions :

    for line in region ['lines']:

        for word in line ['words']:

            license_plate_text +=word ['text']+' '

print ('Detected License Plate Number:',license_plate_text )