from google .cloud import vision

from google .cloud .vision_v1 import types

def image_segmentation (image_path ):

    client =vision .ImageAnnotatorClient ()

    with io .open (image_path ,'rb')as image_file :

        content =image_file .read ()

    image =vision .types .Image (content =content )

    response =client .image_properties (image =image )

    props =response .image_properties_annotation

    print ('Properties:')

    for color in props .dominant_colors .colors :

        print ('Fraction: {}'.format (color .pixel_fraction ))

        print ('\tr: {}'.format (color .color .red ))

        print ('\tb: {}'.format (color .color .blue ))

image_segmentation ('path_to_image.jpg')