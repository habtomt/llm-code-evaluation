def translate_text (text ,target_language ):

    translate_client =translate_v2 .Client ()

    result =translate_client .translate (text ,target_language =target_language )

    return result ["translatedText"]

text_to_translate ="Hello, how are you?"

target_language ="es"

translated_text =translate_text (text_to_translate ,target_language )

print (translated_text )