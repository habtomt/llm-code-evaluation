import boxsdk

from boxsdk import OAuth2 ,Client

oauth2 =OAuth2 (

client_id ='YOUR_CLIENT_ID',

client_secret ='YOUR_CLIENT_SECRET',

)

file_to_encrypt =client .file ('FILE_TO_ENCRYPT_ID')

client .file (file_to_encrypt .id ).update_info ({'inline_extensions':{'encrypted_key':'AES-256'}})

file_to_encrypt .encrypted =True

file_to_encrypt .save ()