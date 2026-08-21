`python

import vimeo_ott

platform =vimeo_ott .Platform (name ="My Video Platform")

video =platform .upload_video (title ="My Video",file_path ="path_to_video_file.mp4")

video .enable_adaptive_bitrate ()

video_url =video .get_url ()

platform .view_video (video_url )