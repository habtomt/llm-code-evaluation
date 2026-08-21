import boto3

import os

aws_access_key ='your_access_key'

aws_secret_key ='your_secret_key'

s3 =boto3 .client ('s3',aws_access_key_id =aws_access_key ,aws_secret_access_key =aws_secret_key ,region_name =aws_region )

bucket_name ='your_bucket_name'

file_name ='your_local_file_path'

key ='remote_file_name'

s3 .upload_file (file_name ,bucket_name ,key )