`python

from google.cloud import vision

from google.cloud.vision import types



def detect_safe_search_uri(uri):

    client = vision.ImageAnnotatorClient()

    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)

    safe = response.safe_search_annotation



    if safe.adult == 5:

        return "Likely inappropriate"

    elif safe.adult == 4:

        return "May be inappropriate"

    else:

        return "Safe for all users"



image_uri = "gs://path_to_your_image.jpg"

result = detect_safe_search_uri(image_uri)

print(result)