import cv2
import pytesseract
from PIL import Image
import re
import os

pytesseract .pytesseract .tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image (image_path ):

    img =cv2 .imread (image_path )

    gray =cv2 .cvtColor (img ,cv2 .COLOR_BGR2GRAY )

    processed_img =cv2 .threshold (gray ,0 ,255 ,cv2 .THRESH_BINARY_INV +cv2 .THRESH_OTSU )[1 ]

    return processed_img

def extract_text_from_image (image_path ):

    processed_img =preprocess_image (image_path )

    text =pytesseract .image_to_string (processed_img )

    return text

def parse_invoice_details (text ):

    invoice_info ={}

    invoice_number_match =re .search (r'Invoice\s+No:\s*(\S+)',text ,re .IGNORECASE )
    if invoice_number_match :
        invoice_info ['invoice_number']=invoice_number_match .group (1 )

    date_match =re .search (r'\b(\d{2}/\d{2}/\d{4})\b',text )
    if date_match :
        invoice_info ['date']=date_match .group (1 )

    price_match =re .findall (r'\$\s*(\d+\.\d+)',text )
    if price_match :
        invoice_info ['prices']=price_match

    vendor_match =re .search (r'Vendor:\s*(\S+)',text ,re .IGNORECASE )
    if vendor_match :
        invoice_info ['vendor']=vendor_match .group (1 )

    item_description_match =re .search (r'Item\s+(\S+):\s*(\S+)',text )
    if item_description_match :
        invoice_info ['item_description']=item_description_match .group (2 )

    return invoice_info

def main ():

    image_path ='path_to_your_invoice_image.jpg'
    if not os .path .isfile (image_path ):
        print ("Error: Image file not found.")
        return

    text =extract_text_from_image (image_path )
    print ("Extracted Text:")
    print (text )

    invoice_details =parse_invoice_details (text )
    print ("Parsed Invoice Details:")
    print (invoice_details )

if __name__ =='__main__':
    main ()