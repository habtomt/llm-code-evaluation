`python

from google.cloud import translate_v2 as translate



def translate_subtitles(subtitle_file, target_language):

    client = translate.Client()

    translated_subtitles = []



    # Read original subtitle file

    with open(subtitle_file, 'r', encoding='utf-8') as file:

        lines = file.readlines()



    # Translate each line and store translated subtitle

        translated_line = client.translate(line, target_language=target_language)

        translated_subtitles.append(translated_line['translatedText'])



    # Write translated subtitle to a new file

    with open(f'translated_{target_language}_{subtitle_file}', 'w', encoding='utf-8') as file:



# Example usage

translate_subtitles('original_subtitle.srt', 'es')  # Translates original subtitle to Spanish