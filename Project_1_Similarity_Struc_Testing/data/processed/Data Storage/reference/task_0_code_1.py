import boto3

import os

s3 =boto3 .client ('s3',

aws_access_key_id ='YOUR_ACCESS_KEY',

aws_secret_access_key ='YOUR_SECRET_ACCESS_KEY')

bucket_name ='your-bucket-name'

file_path ='local-file-to-be-backed-up.txt'

s3 .upload_file (file_path ,bucket_name ,os .path .basename (file_path ))