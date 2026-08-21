import docx
from googletrans import Translator ,LANGUAGES
import pdfplumber
from docx import Document
from fpdf import FPDF
import os

YOUR_API_KEY ='YOUR_API_KEY'

def authenticate_google_translator ():

    try :

        return Translator ()
    except Exception as e :
        print (f"Error authenticating Google Translate API: {e}")
        return None

def translate_text (text ,src_lang ='auto',dest_lang ='en'):

    try :
        translator =authenticate_google_translator ()
        if translator :
            return translator .translate (text ,src =src_lang ,dest =dest_lang ).text
        else :
            return f"Failed to translate text: Authentication error"
    except Exception as e :
        return f"Failed to translate text: {e}"

def translate_docx (input_file ,output_file ,dest_lang ='en'):

    try :

        doc =Document (input_file )
        for para in doc .paragraphs :
            para .text =translate_text (para .text ,dest_lang =dest_lang )
        doc .save (output_file )
        print (f"Translated DOCX saved to {output_file}")
    except Exception as e :
        print (f"Error translating DOCX: {e}")

def translate_pdf (input_file ,output_file ,dest_lang ='en'):

    try :
        with pdfplumber .open (input_file )as pdf :
            translated_text =''
            for page in pdf .pages :
                text =page .extract_text ()
                translated_text +=translate_text (text ,dest_lang =dest_lang )+'\n'

        with open (output_file ,'w')as f :
            f .write (translated_text )
        print (f"Translated PDF text saved to {output_file}. Recreating PDF with original layout is more complex.")
    except Exception as e :
        print (f"Error translating PDF: {e}")

def recreate_pdf (input_file ,output_file ):

    try :
        pdf =FPDF ()
        with pdfplumber .open (input_file )as pdf_doc :
            for page in pdf_doc .pages :
                text =page .extract_text ()
                pdf .add_page ()
                pdf .set_font ("Arial",size =15 )
                for line in text .splitlines ():
                    pdf .cell (200 ,10 ,txt =line ,ln =True ,align ='L')
        pdf .output (output_file )
        print (f"Recreated PDF with translated content saved to {output_file}")
    except Exception as e :
        print (f"Error recreating PDF: {e}")

if __name__ =="__main__":

    translate_docx ('input.docx','translated.docx',dest_lang ='es')

    translate_pdf ('input.pdf','translated.txt',dest_lang ='es')

    recreate_pdf ('input.pdf','translated.pdf')