from google .cloud import vision_v1p3beta1 as vision

import os

os .environ ["GOOGLE_APPLICATION_CREDENTIALS"]="path_to_service_account_key.json"

client =vision .ImageAnnotatorClient ()

def detect_safe_search_uri (uri ):

    image =vision .Image ()
    image .source .image_uri =uri

    response =client .safe_search_detection (image =image )

    safe =response .safe_search_annotation

    if safe .adult ==vision .Likelihood .VERY_LIKELY or safe .adult ==vision .Likelihood .LIKELY :

        print ("Adult content detected")

    if safe .violence ==vision .Likelihood .VERY_LIKELY or safe .violence ==vision .Likelihood .LIKELY :

        print ("Violence detected")

    if safe .racy ==vision .Likelihood .VERY_LIKELY or safe .racy ==vision .Likelihood .LIKELY :

        print ("Racy content detected")

uri ="https://example.com/image.jpg"

detect_safe_search_uri (uri )