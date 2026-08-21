

# Import the necessary libraries

from boxsdk import OAuth2, Client



oauth2 = OAuth2(

    client_id='YOUR_CLIENT_ID',

    client_secret='YOUR_CLIENT_SECRET',

    access_token='YOUR_ACCESS_TOKEN',

)

client = Client(oauth2)



file_id = 'FILE_ID'

file_version = client.file(file_id).add_version('YOUR_NEW_FILE_VERSION')



# Get the version history of the file

version_history = client.file(file_id).get_all_versions()



# Print the version history

for version in version_history:

    print(version.version_number, version.created_at)