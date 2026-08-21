`python

# Import the Vimeo OTT Python SDK

import vimeo_ott



# Set up the client with your API key

client = vimeo_ott.Client(api_key='your_api_key_here')



# Create a new video

video = client.create_video(title='My Video', description='This is my video')



# Upload the video file

video.upload(file_path='path_to_video_file.mp4')

# Categorize the video

video.category = 'Entertainment'



# Save the changes

video.save()



video_url = video.get_adaptive_stream()

print(video_url)