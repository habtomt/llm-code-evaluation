



def translate_text(text, target_language):

    client = translate_v2.Client()

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]



target_language = "es"



translated_text = translate_text(text_to_translate, target_language)

print(translated_text)