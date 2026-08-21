from boxsdk import OAuth2 ,Client

from boxsdk .object .enterprise import Enterprise

oauth2 =OAuth2 (

client_id ='YOUR_CLIENT_ID',

client_secret ='YOUR_CLIENT_SECRET',

access_token ='USER_ACCESS_TOKEN',

)

client =Client (oauth2 )

enterprise =Enterprise (client )

new_user =enterprise .create_user (login ='newuser@example.com',name ='New User')

user_permissions ={

'can_download':True ,

'can_preview':True ,

'can_upload':True

}

client .user (user_id =new_user .object_id ).update_user (user_permissions )

client .folder (folder_id ).add_collaborator (new_user ,'viewer')

client .folder (folder_id ).remove_collaborator (new_user )