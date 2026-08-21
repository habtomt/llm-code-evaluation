from google .cloud import vision
from google .cloud .vision import types

def compress_image (input_file_path ,output_file_path ,quality ):
    import io
    from PIL import Image

    client =vision .ImageAnnotatorClient ()

    with io .open (input_file_path ,'rb')as image_file :
        content =image_file .read ()

    image =types .Image (content =content )
    response =client .safe_search_detection (image =image )
    safe_search =response .safe_search_annotation

    if safe_search .violence .value <3 :
        img =Image .open (input_file_path )
        img .save (output_file_path ,optimize =True ,quality =quality )
        print (f"Image compressed and saved to {output_file_path}")
    else :
        print ("Image contains violence, compression not allowed.")