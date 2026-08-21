`python

from google .cloud import vision

client =vision .ImageAnnotatorClient ()

def content_moderation (image_uri ):

    image =vision .Image ()

    if response .safe_search_annotation .adult ==5 or response .safe_search_annotation .violence ==5 :

        return "Flag as harmful content"

    else :

        return "No harmful content detected"