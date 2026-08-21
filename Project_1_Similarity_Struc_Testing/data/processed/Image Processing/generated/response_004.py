import cv2
import numpy as np

def kmeans_segmentation (image_path ,K =3 ):

    image =cv2 .imread (image_path )
    if image is None :
        print ("Error: Image not found.")
        return

    pixel_values =image .reshape ((-1 ,3 ))
    pixel_values =np .float32 (pixel_values )

    criteria =(cv2 .TERM_CRITERIA_EPS +cv2 .TERM_CRITERIA_MAX_ITER ,100 ,0.2 )
    _ ,labels ,centers =cv2 .kmeans (pixel_values ,K ,None ,criteria ,10 ,cv2 .KMEANS_RANDOM_CENTERS )

    centers =np .uint8 (centers )

    segmented_image =centers [labels .flatten ()]

    segmented_image =segmented_image .reshape (image .shape )

    cv2 .imshow ('Original Image',image )
    cv2 .imshow ('Segmented Image',segmented_image )
    cv2 .waitKey (0 )
    cv2 .destroyAllWindows ()

kmeans_segmentation ('path_to_your_image.jpg',K =3 )