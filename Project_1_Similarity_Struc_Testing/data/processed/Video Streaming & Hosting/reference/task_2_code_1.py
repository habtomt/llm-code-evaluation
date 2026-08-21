`python

import vimeo

client = vimeo.ViClient(

    client_id='your_client_id',

    client_secret='your_client_secret',

    access_token='your_access_token'

)

video_uri = client.upload(

    file_path='path_to_user_video_file.mp4',

)

    uri=video_uri,

    video_name='User Generated Video',

    privacy='anybody'

)