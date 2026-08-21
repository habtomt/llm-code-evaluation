`python

# Import the Vimeo OTT Python client

from vimeo_ott import VimeoOTT



# Initialize the client with your Vimeo OTT API credentials

client = VimeoOTT(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')



# Create a new interactive video with quizzes, annotations, and clickable links

interactive_video_data = {

    "title": "Interactive Video Title",

    "video_file_path": "/path/to/video.mp4",

    "quizzes": [

        {

            "question": "What is 1 + 1?",

            "options": ["1", "2", "3", "4"],

            "correct_option": "2"

        }

    ],

    "annotations": [

        {

            "time": 10,  # Time in seconds

            "content": "This is an annotation at 10 seconds"

        }

    ],

    "clickable_links": [

            "time": 20,  # Time in seconds

            "url": "https://example.com",

            "label": "Clickable Link"

        }

    ]

}



# Upload the interactive video to Vimeo OTT

response = client.create_interactive_video(interactive_video_data)



# Print the response

print(response)