from PIL import Image
import os

def reduce_image_size (input_path ,output_path ,quality =85 ):

    try :

        with Image .open (input_path )as img :

            if img .format =='JPEG'or img .format =='JPG':

                img .save (output_path ,'JPEG',quality =quality ,optimize =True )
            elif img .format =='PNG':

                img .save (output_path ,'PNG',optimize =True )
            else :

                img .save (output_path ,'PNG',optimize =True )
        print (f"Image successfully compressed and saved at: {output_path}")
    except Exception as e :
        print (f"An error occurred: {e}")

reduce_image_size ('path/to/input/image.jpg','path/to/output/image.jpg',quality =75 )