

import io

from PIL import Image



def compress_image(input_file, output_file, quality=75):

    with io.open(input_file, 'rb') as img_file:

        img_data = img_file.read()



    img = Image.open(io.BytesIO(img_data))



    img.save(output_file, quality=quality)

# Example usage

input_file = 'input_image.jpg'

output_file = 'compressed_image.jpg'

compress_image(input_file, output_file)