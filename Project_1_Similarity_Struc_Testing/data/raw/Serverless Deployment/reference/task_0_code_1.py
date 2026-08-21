`python

from http import HTTPStatus

from vercel import Now, Response

from PIL import Image

from io import BytesIO

import requests



def process_image(request):

    image_url = request.query.get('url')

    response = requests.get(image_url)

    if response.status_code == 200:

        image = Image.open(BytesIO(response.content))

        # Perform image processing tasks here

        # e.g. image resizing, filtering, etc.



        # Return the processed image

        output = BytesIO()

        image.save(output, format="JPEG")

        return Response(output.getvalue(), status=HTTPStatus.OK, content_type="image/jpeg")

        return Response("Failed to process image", status=HTTPStatus.BAD_REQUEST)

  

now = Now()

now.deploy(process_image, name="image-processing-service")