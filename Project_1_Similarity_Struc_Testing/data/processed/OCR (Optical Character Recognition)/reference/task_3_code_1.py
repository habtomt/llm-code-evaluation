import requests

subscription_key ='YOUR_SUBSCRIPTION_KEY'

endpoint ='YOUR_ENDPOINT'

ocr_url =f"{endpoint}/vision/v3.1/ocr"

headers ={

'Ocp-Apim-Subscription-Key':subscription_key ,

'Content-Type':'application/json'

}

image_url ='URL_OF_YOUR_IMAGE'

data ={'url':image_url }

response =requests .post (ocr_url ,headers =headers ,json =data )

analysis =response .json ()

extracted_text =''

for region in analysis ['regions']:

    for line in region ['lines']:

        for word in line ['words']:

            extracted_text +=word ['text']+' '

print (extracted_text )