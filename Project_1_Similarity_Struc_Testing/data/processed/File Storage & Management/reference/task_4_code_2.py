import boxsdk

client =boxsdk .Client (CLIENT_ID ,CLIENT_SECRET ,enterprise_auth =True )

root_folder =client .folder (folder_id ='0').get ()

with open ('large_file.zip','rb')as large_file :

    large_file_uploaded =root_folder .upload (large_file ,file_name ='large_file.zip')

retrieved_file =root_folder .get_file (file_id ='12345').content ()

additional_folder =root_folder .create_subfolder ('additional_data_folder')

large_scale_file_operations =root_folder .get_items (limit =1000 )