

import boxsdk

from boxsdk import OAuth2, Client



# Generate access token and authenticate client

oauth2 = OAuth2(

    client_id='YOUR_CLIENT_ID',

    client_secret='YOUR_CLIENT_SECRET',

)



# Encrypt file in transit

file_to_encrypt = client.file('FILE_TO_ENCRYPT_ID')

client.file(file_to_encrypt.id).update_info({'inline_extensions': {'encrypted_key': 'AES-256'}})



# Encrypt file at rest

file_to_encrypt.encrypted = True

file_to_encrypt.save()