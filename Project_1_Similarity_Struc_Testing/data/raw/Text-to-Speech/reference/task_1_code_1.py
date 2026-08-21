`python

from google.cloud import texttospeech



def synthesize_text(text, language_code, ssml_voice_gender):

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open('output.wav', 'wb') as out:

        out.write(response.audio_content)

        print('Audio content written to file "output.wav"')



query = "How can I return a product?"

language_code = "en-US"

ssml_voice_gender = texttospeech.SsmlVoiceGender.FEMALE



synthesize_text(query, language_code, ssml_voice_gender)