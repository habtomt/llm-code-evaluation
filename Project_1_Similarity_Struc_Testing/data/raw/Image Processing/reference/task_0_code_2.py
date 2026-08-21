from google.cloud import vision
import io

def detect_faces(image_path):
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    if faces:
        for face in faces:
            print("Joy: {}".format(face.joy_likelihood))
            print("Sorrow: {}".format(face.sorrow_likelihood))
            print("Anger: {}".format(face.anger_likelihood))
            print("Surprise: {}".format(face.surprise_likelihood))

detect_faces("path_to_image.jpg")