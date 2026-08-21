`python

from google.cloud import texttospeech

def synthesize_speech(text, output_filename):

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(

        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

    )

    audio_config = texttospeech.AudioConfig(

        audio_encoding=texttospeech.AudioEncoding.MP3

    response = client.synthesize_speech(

        input=input_text, voice=voice, audio_config=audio_config

    )

    with open(output_filename, "wb") as out:

        print(f'Audio content written to file {output_filename}')

text = "Thank you for contacting our customer service. How can we assist you today?"

output_filename = "customer_service_response.mp3"

synthesize_speech(text, output_filename)