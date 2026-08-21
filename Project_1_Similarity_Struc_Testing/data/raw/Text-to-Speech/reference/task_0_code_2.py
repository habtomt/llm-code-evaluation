`python

from google.cloud import texttospeech



client = texttospeech.TextToSpeechClient()



input_text = "Hello, welcome to the E-Learning Application. Today we will be learning about Text-to-Speech technology and its applications."



synthesis_input = texttospeech.SynthesisInput(text=input_text)



    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

)



audio_config = texttospeech.AudioConfig(

    audio_encoding=texttospeech.AudioEncoding.MP3

)



response = client.synthesize_speech(

    input=synthesis_input, voice=voice, audio_config=audio_config

)



with open("output.mp3", "wb") as out:

    out.write(response.audio_content)