

# Import the Box SDK

from boxsdk import OAuth2, Client



# Set up authentication and create a client connection

auth = OAuth2(

    client_id='YOUR_CLIENT_ID',

    client_secret='YOUR_CLIENT_SECRET',

    access_token='YOUR_ACCESS_TOKEN',

)

client = Client(auth)



# Upload a file to Box

folder_id = 'folder_id_to_upload_to'

file_name = 'name_of_file_on_box'



# Download a file from Box

file_id = 'file_id_to_download'

file_content = client.file(file_id).content()

with open('downloaded_file', 'wb') as downloaded_file:

    downloaded_file.write(file_content)



# Manage metadata in Box

file_id = 'file_id_to_manage_metadata'

metadata = {'key1': 'value1', 'key2': 'value2'}

client.file(file_id).update_info({'metadata': metadata})