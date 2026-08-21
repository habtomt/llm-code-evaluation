import base64
from io import BytesIO
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from flask import Flask ,request ,jsonify
from flask_cors import CORS

app =Flask (__name__ )
CORS (app )

def process_image (image_data ):
    try :

        image_buffer =BytesIO (base64 .b64decode (image_data ))

        image =Image .open (image_buffer )

        image =image .resize ((200 ,200 ))

        image =image .convert ('L')

        enhancer =ImageEnhance .Contrast (image )
        image =enhancer .enhance (1.5 )

        image =image .filter (ImageFilter .GaussianBlur (radius =2 ))

        image_buffer =BytesIO ()
        image .save (image_buffer ,format ='PNG')
        image_data =base64 .b64encode (image_buffer .getvalue ()).decode ('utf-8')

        return {
        'image':image_data
        }
    except Exception as e :
        return {
        'error':'Image processing failed',
        'details':str (e )
        }

@app .route ('/process_image',methods =['POST'])
def handle_request ():
    try :

        image_data =request .get_json ()['image']

        result =process_image (image_data )

        return jsonify (result ),200
    except Exception as e :
        return jsonify ({
        'error':'Invalid request',
        'details':str (e )
        }),500

if __name__ =='__main__':
    app .run (debug =True )