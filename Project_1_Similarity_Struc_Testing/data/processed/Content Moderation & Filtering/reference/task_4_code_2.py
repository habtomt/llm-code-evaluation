`python

from google .cloud .vision_v1 import enums

def detect_safe_search_uri (uri ):

    client =vision .ImageAnnotatorClient ()

    image =vision .Image ()

    image .source .image_uri =uri

    response =client .safe_search_detection (image =image )

    safe_search =response .safe_search_annotation

    if safe_search .adult ==enums .Likelihood .VERY_LIKELY or safe_search .violence ==enums .Likelihood .VERY_LIKELY or safe_search .racy ==enums .Likelihood .VERY_LIKELY :

    elif safe_search .adult ==enums .Likelihood .POSSIBLE or safe_search .violence ==enums .Likelihood .POSSIBLE or safe_search .racy ==enums .Likelihood .POSSIBLE :

        return "This content may not be suitable for the website."

    else :

        return "This content is suitable for the website."

result =detect_safe_search_uri ("gs://bucket_name/object_name.jpg")

print (result )