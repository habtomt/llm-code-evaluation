`python

from google.cloud import vision

from google.cloud.vision_v1.types import AnnotateImageRequest, SafeSearchAnnotation



def detect_safe_search_uri(uri):

    client = vision.ImageAnnotatorClient()

    image = vision.Image()

    image.source.image_uri = uri



    response = client.annotate_image(

        request={

            "image": image,

            "features": [{"type": vision.Feature.Type.SAFE_SEARCH_DETECTION}],

        }



    safe_search = response.safe_search_annotation

    return safe_search



uri = "gs://your_bucket_name/your_image.jpg"

safe_search_result = detect_safe_search_uri(uri)