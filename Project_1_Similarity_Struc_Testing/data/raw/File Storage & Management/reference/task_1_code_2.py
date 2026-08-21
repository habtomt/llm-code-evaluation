

import requests



class BoxFileVersioning:

    def __init__(self, api_key):

        self.api_key = api_key

        self.base_url = "https://api.box.com/2.0/"



    def get_file_versions(self, file_id):

        url = self.base_url + f"files/{file_id}/versions"

        headers = {

            "Authorization": f"Bearer {self.api_key}"

        }

        response = requests.get(url, headers=headers)

        return response.json()



    def upload_new_version(self, file_id, file_path):

        url = self.base_url + f"files/{file_id}/content"

        headers = {

            "Authorization": f"Bearer {self.api_key}"

        }

        files = {

        }

        response = requests.post(url, headers=headers, files=files)

        return response.json()



    def restore_to_version(self, file_id, version_id):

        url = self.base_url + f"files/{file_id}/content"

        headers = {

            "Authorization": f"Bearer {self.api_key}"

        }

        data = {

            'type': 'file_version',

            'id': version_id

        }

        return response.json()



# Example Usage

api_key = "YOUR_BOX_API_KEY"

box = BoxFileVersioning(api_key)



# Get file versions

file_id = "FILE_ID"

versions = box.get_file_versions(file_id)

print(versions)



# Upload new version

file_path = "path_to_file"

upload_response = box.upload_new_version(file_id, file_path)

print(upload_response)



# Restore to a specific version

version_id = "VERSION_ID"

restore_response = box.restore_to_version(file_id, version_id)

print(restore_response)