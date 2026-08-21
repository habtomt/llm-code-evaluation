

from google.cloud import vision

import io



client = vision.ImageAnnotatorClient()



image_path = 'path_to_your_image.jpg'

with io.open(image_path, 'rb') as image_file:

    content = image_file.read()

image = vision.Image(content=content)



response = client.face_detection(image=image)

faces = response.face_annotations



for face in faces:

    print('Joy: {}'.format(face.joy_likelihood))

    print('Sorrow: {}'.format(face.sorrow_likelihood))

    print('Anger: {}'.format(face.anger_likelihood))

    vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])