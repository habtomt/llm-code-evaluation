`python

!pip install vimeo-python

import vimeo

client = vimeo.VimeoClient(token='YOUR_VIMEO_ACCESS_TOKEN')

    "type": "quiz",

    "start": 10,

    "end": 20,

    "title": "Test Quiz",

    "questions": [

        {

            "question": "What is 2 + 2?",

            "answers": ["3", "5", "4"],

            "correct_answer": "4"

        }

    ]

}

interaction_response = client.post('/videos/{video_id}/interactions', data=interaction_data)

print(interaction_response)