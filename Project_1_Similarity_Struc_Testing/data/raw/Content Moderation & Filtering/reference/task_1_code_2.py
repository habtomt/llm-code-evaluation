`python

from google.cloud import vision



client = vision.ImageAnnotatorClient()

def detect_safe_search_uri(uri):

    image = vision.Image()

    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)

    

    print('Safe search:')

    

    for result in response.safe_search_annotation:

        print('Adult:', vision.Likelihood(result.adult).name)

        print('Spoof:', vision.Likelihood(result.spoof).name)

        print('Medical:', vision.Likelihood(result.medical).name)

        print('Racy:', vision.Likelihood(result.racy).name)