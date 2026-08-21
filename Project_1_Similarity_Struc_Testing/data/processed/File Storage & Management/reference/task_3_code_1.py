import boxsdk

auth =boxsdk .JWTAuth (

client_id ='YOUR_CLIENT_ID',

client_secret ='YOUR_CLIENT_SECRET',

enterprise_id ='YOUR_ENTERPRISE_ID',

jwt_key_id ='YOUR_JWT_KEY_ID',

rsa_private_key_file_sys_path ='PATH_TO_PRIVATE_KEY'

)

client =boxsdk .Client (auth )

file_info =client .file (file_id ='FILE_ID').get ()

encrypted_file_url =file_info .get_url ()

file =client .file (file_id ='FILE_ID').get ()

file .enable_shield_encryption ()