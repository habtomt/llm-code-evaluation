import torch
from PIL import Image
import os
import pandas as pd

model =torch .hub .load ('ultralytics/yolov5','yolov5s',pretrained =True )

def detect_objects (image_path ):
    try :

        img =Image .open (image_path )

        results =model (img )

        results .print ()

        results .show ()

        df =results .pandas ().xyxy [0 ]

        return df

    except Exception as e :
        print (f"An error occurred: {e}")

image_path ='path/to/your/image.jpg'
result_df =detect_objects (image_path )

if result_df is not None :
    print ("Detected objects:")
    print (result_df )

else :
    print ("No objects detected or an error occurred.")