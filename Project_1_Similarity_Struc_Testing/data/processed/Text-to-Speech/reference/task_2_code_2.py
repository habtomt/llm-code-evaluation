`python

from google .cloud import texttospeech

input_text =texttospeech .SynthesisInput (text ="Hello, world!")

voice =texttospeech .VoiceSelectionParams (

language_code ="en-US",ssml_gender =texttospeech .SsmlVoiceGender .NEUTRAL

)

audio_config =texttospeech .AudioConfig (

audio_encoding =texttospeech .AudioEncoding .MP3

)

response =client .synthesize_speech (

input =input_text ,voice =voice ,audio_config =audio_config

)

    out .write (response .audio_content )

    print ('Audio content written to file "output.mp3"')