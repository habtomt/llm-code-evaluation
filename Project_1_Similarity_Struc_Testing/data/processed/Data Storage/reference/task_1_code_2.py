import boto3

s3 =boto3 .resource ('s3')

bucket_name ='my_database_bucket'

file_path ='local_database_backup.sql'

bucket .upload_file (file_path ,'database_backups/local_database_backup.sql')