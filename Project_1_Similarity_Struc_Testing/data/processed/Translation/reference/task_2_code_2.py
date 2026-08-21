`python

from google .cloud import translate_v2 as translate

def translate_subtitles (subtitle_file ,target_language ):

    client =translate .Client ()

    translated_subtitles =[]

    with open (subtitle_file ,'r',encoding ='utf-8')as file :

        lines =file .readlines ()

        translated_line =client .translate (line ,target_language =target_language )

        translated_subtitles .append (translated_line ['translatedText'])

    with open (f'translated_{target_language}_{subtitle_file}','w',encoding ='utf-8')as file :

translate_subtitles ('original_subtitle.srt','es')