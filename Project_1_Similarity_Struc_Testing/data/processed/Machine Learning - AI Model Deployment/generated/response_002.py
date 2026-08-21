import numpy as np
from PIL import Image
import tensorflow as tf
import os
import subprocess

def load_model (tflite_model_path ):
    interpreter =tf .lite .Interpreter (model_path =tflite_model_path )
    interpreter .allocate_tensors ()
    return interpreter

def get_tensors (interpreter ):
    input_details =interpreter .get_input_details ()
    output_details =interpreter .get_output_details ()
    return input_details ,output_details

def load_input_image (image_path ):

    img =Image .open (image_path ).resize ((224 ,224 ))

    input_data =np .array (img ,dtype =np .float32 )

    input_data =(input_data /127.5 )-1.0

    input_data =np .expand_dims (input_data ,axis =0 )
    return input_data

def run_inference (interpreter ,image_path ):
    input_data =load_input_image (image_path )

    input_details ,_ =get_tensors (interpreter )
    assert input_details [0 ]['shape']==input_data .shape
    assert input_details [0 ]['dtype']==input_data .dtype

    interpreter .set_tensor (input_details [0 ]['index'],input_data )

    interpreter .invoke ()

    output_data =interpreter .get_tensor (output_details [0 ]['index'])

    predicted_class =np .argmax (output_data )
    return predicted_class

def train_and_export_model ():

    pass

def convert_model ():

    converter =tf .lite .TFLiteConverter .from_keras_model (tf .keras .applications .MobileNetV2 (weights ='imagenet',include_top =True ))
    converter .optimizations =[tf .lite .Optimize .DEFAULT ]
    tflite_model =converter .convert ()
    with open ("mobilenet_v2.tflite","wb")as f :
        f .write (tflite_model )

def deploy_model ():

    subprocess .run (["scp","mobilenet_v2.tflite","edge_device:~"])

if __name__ =="__main__":

    convert_model ()

    interpreter =load_model ("mobilenet_v2.tflite")

    input_details ,output_details =get_tensors (interpreter )

    image_path ="example.jpg"

    predicted_class =run_inference (interpreter ,image_path )
    print (f"Predicted class: {predicted_class}")