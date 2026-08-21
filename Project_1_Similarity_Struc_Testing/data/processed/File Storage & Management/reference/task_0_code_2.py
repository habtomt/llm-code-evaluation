from boxsdk import OAuth2 ,Client

client_id ='YOUR_CLIENT_ID'

client_secret ='YOUR_CLIENT_SECRET'

access_token ='YOUR_ACCESS_TOKEN'

oauth2 =OAuth2 (

client_id =client_id ,

access_token =access_token ,

)

client =Client (oauth2 )

def upload_file_to_box (file_path ,folder_id ):

    file_name =file_path .split ('/')[-1 ]

    folder =client .folder (folder_id )

    uploaded_file =folder .upload (file_path ,file_name )

    return uploaded_file .id ,uploaded_file .name

def download_file_from_box (file_id ,save_to_path ):

    file =client .file (file_id ).get ()

    open (save_to_path ,'wb').write (file .content ())

def update_file_metadata (file_id ,metadata ):

    file =client .file (file_id ).update_info (metadata )

    return file .id

file_path ='path_to_your_file'

folder_id ='your_folder_id'

uploaded_id ,uploaded_name =upload_file_to_box (file_path ,folder_id )

download_file_from_box (uploaded_id ,'path_to_save_downloaded_file')

updated_file_id =update_file_metadata (uploaded_id ,{'new_metadata':'value'})