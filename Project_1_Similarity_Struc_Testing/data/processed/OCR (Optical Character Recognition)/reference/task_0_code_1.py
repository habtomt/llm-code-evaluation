import requests

subscription_key ='your_subscription_key'

endpoint ='your_azure_endpoint'

ocr_url =f'{endpoint}/vision/v3.1/ocr'

image_path ='path_to_your_invoice_image.jpg'

headers ={'Ocp-Apim-Subscription-Key':subscription_key ,'Content-Type':'application/octet-stream'}

image_data =open (image_path ,'rb').read ()

response =requests .post (ocr_url ,headers =headers ,data =image_data )

response .raise_for_status ()

analysis =response .json ()

for region in analysis ['regions']:

    for line in region ['lines']:

        for word in line ['words']:

            print (word ['text'])