`python



def translate_text(text, target_language):

    client = translate.TranslationServiceClient()

    parent = client.location_path("[PROJECT_ID]", "[LOCATION]")

    response = client.translate_text(

        request={

            "parent": parent,

            "contents": [text],

        }

    )



    for translation in response.translations:

        return translation.translated_text



translated_text = translate_text("Hello, world!", "fr")

print(translated_text)