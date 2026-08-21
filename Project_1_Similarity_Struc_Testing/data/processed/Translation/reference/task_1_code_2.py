`python

from google .cloud import translate_v2 as translate

def translate_text (text ,target_language ):

    translate_client =translate .Client ()

    result =translate_client .translate (text ,target_language =target_language )

text_to_translate ="Hello, welcome to our website"

target_language ="es"

print (translated_text )