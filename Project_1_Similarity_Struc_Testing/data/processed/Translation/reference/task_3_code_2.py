`python

from google .cloud import translate

def translate_document (input_text ,target_language ):

    client =translate .TranslationServiceClient ()

    location ='us-central1'

    response =client .translate_text (

    request ={

    "parent":parent ,

    "mime_type":"text/plain",

    "target_language_code":target_language ,

    }

    )

    translated_text =response .translations [0 ].translated_text

    return translated_text