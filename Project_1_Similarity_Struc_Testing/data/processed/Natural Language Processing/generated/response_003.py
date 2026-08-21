from google .cloud import translate_v2 as translate
import os

def translate_text (text ,target_language ):
    try :

        translate_client =translate .Client ()

        result =translate_client .translate (text ,target_lang =target_language )

        print ("Text: {}".format (result ["input"]))
        print ("Translation: {}".format (result ["translatedText"]))
        print ("Detected source language: {}".format (result ["detectedSourceLanguage"]))

    except Exception as e :
        print ("Error translating text: {}".format (e ))

if __name__ =="__main__":

    os .environ ['GOOGLE_APPLICATION_CREDENTIALS']='/path/to/your/service_account.json'

    text_to_translate ="Hello, how are you?"
    target_language_code ="es"

    translate_text (text_to_translate ,target_language_code )