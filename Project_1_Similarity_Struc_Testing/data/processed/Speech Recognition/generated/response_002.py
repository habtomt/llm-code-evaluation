from flask import Flask ,request ,jsonify
from google .cloud import dialogflow_v2 as dialogflow
from google .cloud import texttospeech
import os
import base64
import json
import logging

logging .basicConfig (level =logging .INFO )
logger =logging .getLogger (__name__ )

app =Flask (__name__ )

os .environ ["GOOGLE_APPLICATION_CREDENTIALS"]="path/to/your/service-account-file.json"

dialogflow_client =dialogflow .SessionsClient ()
project_id ="your-dialogflow-project-id"

tts_client =texttospeech .TextToSpeechClient ()

def detect_intent_texts (session_id ,text ):

    try :
        session =dialogflow_client .session_path (project_id ,session_id )
        text_input =dialogflow .types .TextInput (text =text ,language_code ="en-US")
        query_input =dialogflow .types .QueryInput (text =text_input )

        response =dialogflow_client .detect_intent (session =session ,query_input =query_input )
        return response .query_result .fulfillment_text
    except Exception as e :
        logger .error (f"Error detecting intent: {str(e)}")
        return "Sorry, I did not understand your request."

def synthesize_speech (text ):

    try :
        synthesis_input =texttospeech .SynthesisInput (text =text )
        voice =texttospeech .VoiceSelectionParams (language_code ="en-US",ssml_gender =texttospeech .SsmlVoiceGender .NEUTRAL )
        audio_config =texttospeech .AudioConfig (audio_encoding =texttospeech .AudioEncoding .MP3 )

        response =tts_client .synthesize_speech (input =synthesis_input ,voice =voice ,audio_config =audio_config )
        audio_content =base64 .b64encode (response .audio_content ).decode ('utf-8')
        return audio_content
    except Exception as e :
        logger .error (f"Error synthesizing speech: {str(e)}")
        return "Sorry, I'm experiencing a technical issue."

@app .route ('/webhook',methods =['POST'])
def webhook ():

    try :
        session_id =request .json .get ('session_id','default')
        user_input =request .json .get ('query','')

        response_text =detect_intent_texts (session_id ,user_input )

        audio_content =synthesize_speech (response_text )

        return jsonify ({
        'response_text':response_text ,
        'audio_content':audio_content
        })
    except Exception as e :
        logger .error (f"Error handling webhook request: {str(e)}")
        return jsonify ({'error':'Sorry, I'm experiencing a technical issue .'})

if __name__ =='__main__':
    app .run (debug =True )