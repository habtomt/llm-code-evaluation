

import json

from msrest.authentication import CognitiveServicesCredentials



# Replace with your own keys and endpoint

subscription_key = 'YOUR_SUBSCRIPTION_KEY'

endpoint = 'YOUR_ENDPOINT'



image_url = 'URL_OF_YOUR_IMAGE'



credentials = CognitiveServicesCredentials(subscription_key)

client = ComputerVisionClient(endpoint, credentials)



handwritten_text_result = client.read(image_url, raw=True)



operation_location_remote = handwritten_text_result.headers["Operation-Location"]

operation_id = operation_location_remote.split("/")[-1]



result = client.get_read_result(operation_id)

result_response = result.as_dict()



for read_result in result_response["analyzeResult"]["readResults"]:

    for line in read_result["lines"]:

        print(line["text"])