
import boto3

import os



# Establish connection to Amazon S3

s3 = boto3.client('s3', 

                  aws_access_key_id='YOUR_ACCESS_KEY',

                  aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')

# Define the bucket name

bucket_name = 'your-bucket-name'

# Define the local file to be uploaded

file_path = 'local-file-to-be-backed-up.txt'



# Upload file to Amazon S3 bucket

s3.upload_file(file_path, bucket_name, os.path.basename(file_path))