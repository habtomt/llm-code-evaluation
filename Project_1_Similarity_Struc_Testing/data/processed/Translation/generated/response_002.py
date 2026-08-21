import pysrt
from googletrans import Translator
import logging

logging .basicConfig (level =logging .INFO )
logger =logging .getLogger (__name__ )

def translate_subtitle (input_file ,output_file ,target_language ):

    translator =Translator ()

    try :

        subs =pysrt .open (input_file )

        for sub in subs :

            translation =translator .translate (sub .text ,dest =target_language ).text

            sub .text =translation

        subs .save (output_file ,encoding ='utf-8')
        logger .info (f'Translation complete. Output saved to {output_file}')
    except Exception as e :
        logger .error (f'Failed to translate subtitles: {e}')

if __name__ =="__main__":

    input_srt_file ='input_subtitles.srt'
    output_srt_file ='translated_subtitles.srt'
    target_lang ='fr'

    translate_subtitle (input_srt_file ,output_srt_file ,target_lang )