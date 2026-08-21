`python

from vimeo_ott import VimeoOTT

client = VimeoOTT(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')

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

            "time": 10,

            "content": "This is an annotation at 10 seconds"

        }

    ],

    "clickable_links": [

            "time": 20,

            "url": "https://example.com",

            "label": "Clickable Link"

        }

    ]

}

response = client.create_interactive_video(interactive_video_data)

print(response)