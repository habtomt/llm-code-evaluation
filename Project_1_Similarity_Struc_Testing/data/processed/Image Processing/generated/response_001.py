from PIL import Image ,ImageEnhance

def enhance_image (input_image_path ,output_image_path ,brightness =1.0 ,contrast =1.0 ,sharpness =1.0 ):

    try :
        with Image .open (input_image_path )as img :

            enhancer =ImageEnhance .Brightness (img )
            img =enhancer .enhance (brightness )

            enhancer =ImageEnhance .Contrast (img )
            img =enhancer .enhance (contrast )

            enhancer =ImageEnhance .Sharpness (img )
            img =enhancer .enhance (sharpness )

            img .save (output_image_path )
            print (f"Enhanced image saved to {output_image_path}")
    except Exception as e :
        print (f"An error occurred: {e}")

input_image_path ='input.jpg'
output_image_path ='output.jpg'

brightness_factor =1.2
contrast_factor =1.5
sharpness_factor =2.0

enhance_image (input_image_path ,output_image_path ,brightness_factor ,contrast_factor ,sharpness_factor )