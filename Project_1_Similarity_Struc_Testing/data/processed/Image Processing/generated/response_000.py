import cv2

face_cascade =cv2 .CascadeClassifier (cv2 .data .haarcascades +'haarcascade_frontalface_default.xml')

def detect_faces (image_path ):
    try :

        image =cv2 .imread (image_path )

        if image is None :
            print ('Error opening image!')
            return

        gray =cv2 .cvtColor (image ,cv2 .COLOR_BGR2GRAY )

        faces =face_cascade .detectMultiScale (gray ,scaleFactor =1.1 ,minNeighbors =5 ,minSize =(30 ,30 ))

        print (f"Found {len(faces)} faces!")

        for (x ,y ,w ,h )in faces :
            cv2 .rectangle (image ,(x ,y ),(x +w ,y +h ),(255 ,0 ,0 ),2 )

        cv2 .imshow ('Faces found',image )
        cv2 .waitKey (0 )
        cv2 .destroyAllWindows ()

    except Exception as e :
        print (f"An error occurred: {e}")

image_path ='path_to_your_image.jpg'
detect_faces (image_path )