`python

from google .cloud import vision

from google .cloud .vision_v1 import types

def detect_safe_search_uri (uri ):

    client =vision .ImageAnnotatorClient ()

    image =vision .types .Image ()

    image .source .image_uri =uri

    response =client .safe_search_detection (image =image )

    safe =response .safe_search_annotation

    return {'adult':vision .Likelihood (safe .adult ).name ,

    'spoof':vision .Likelihood (safe .spoof ).name ,

    'medical':vision .Likelihood (safe .medical ).name ,

    'racy':vision .Likelihood (safe .racy ).name }