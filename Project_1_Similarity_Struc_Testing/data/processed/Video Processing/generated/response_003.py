import cv2
import numpy as np

def adjust_brightness_contrast (image ,brightness =0 ,contrast =0 ):

    brightness =int ((brightness -0.5 )*255 )
    contrast =int ((contrast -0.5 )*255 )

    adjusted =cv2 .convertScaleAbs (image ,alpha =1 +contrast /127.0 ,beta =brightness )
    return adjusted

def enhance_video (input_path ,output_path ):

    cap =cv2 .VideoCapture (input_path )

    frame_count =int (cap .get (cv2 .CAP_PROP_FRAME_COUNT ))
    fps =cap .get (cv2 .CAP_PROP_FPS )
    width =int (cap .get (cv2 .CAP_PROP_FRAME_WIDTH ))
    height =int (cap .get (cv2 .CAP_PROP_FRAME_HEIGHT ))

    fourcc =cv2 .VideoWriter_fourcc (*'XVID')
    out =cv2 .VideoWriter (output_path ,fourcc ,fps ,(width ,height ))

    while cap .isOpened ():
        ret ,frame =cap .read ()
        if not ret :
            break

        lab =cv2 .cvtColor (frame ,cv2 .COLOR_BGR2Lab )

        l ,a ,b =cv2 .split (lab )

        clahe =cv2 .createCLAHE (clipLimit =3.0 ,tileGridSize =(8 ,8 ))
        cl =clahe .apply (l )
        lab =cv2 .merge ((cl ,a ,b ))

        frame_clahe =cv2 .cvtColor (lab ,cv2 .COLOR_Lab2BGR )

        frame_adj =adjust_brightness_contrast (frame_clahe ,brightness =0.5 ,contrast =0.5 )

        kernel =np .array ([[0 ,-1 ,0 ],[-1 ,5 ,-1 ],[0 ,-1 ,0 ]])
        frame_sharp =cv2 .filter2D (frame_adj ,-1 ,kernel )

        out .write (frame_sharp )

    cap .release ()
    out .release ()

input_video_path ='input_video.mp4'
output_video_path ='enhanced_video.mp4'

enhance_video (input_video_path ,output_video_path )