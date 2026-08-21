`python



    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]



user_language = "fr"  # Assuming user selects French as their preferred language

text_to_translate = "Hello, how are you?"  # Assuming this is a part of the website content

translated_text = translate_text(user_language, text_to_translate)

print(translated_text)