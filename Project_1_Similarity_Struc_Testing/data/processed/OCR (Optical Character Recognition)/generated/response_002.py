import cv2
from PIL import Image
import pytesseract
import os

pytesseract .pytesseract .tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image (image_path ):

    try :

        image =cv2 .imread (image_path )

        if image is None :
            print (f"Error: Unable to load image {image_path}")
            return None

        gray =cv2 .cvtColor (image ,cv2 .COLOR_BGR2GRAY )

        _ ,binary_image =cv2 .threshold (gray ,128 ,255 ,cv2 .THRESH_BINARY_INV +cv2 .THRESH_OTSU )

        return binary_image

    except Exception as e :
        print (f"Error preprocessing image: {e}")
        return None

def recognize_text (image_path ):

    try :

        processed_image =preprocess_image (image_path )

        if processed_image is None :
            return None

        pil_image =Image .fromarray (processed_image )

        text =pytesseract .image_to_string (pil_image )

        return text

    except Exception as e :
        print (f"Error recognizing text: {e}")
        return None

image_path ='handwritten_sample.png'
recognized_text =recognize_text (image_path )

if recognized_text is not None :
    print ("Recognized Text:")
    print (recognized_text )