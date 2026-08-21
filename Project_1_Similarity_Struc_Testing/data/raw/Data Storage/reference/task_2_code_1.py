`python

import boto3



# Create a S3 client

s3 = boto3.client('s3')



# Create a bucket

s3.create_bucket(Bucket=bucket_name)



# Upload a file

file_path = 'path_to_file'

file_key = 'file_key'

s3.upload_file(file_path, bucket_name, file_key)



# Download a file

download_path = 'path_to_save_file'

s3.download_file(bucket_name, file_key, download_path)

# Delete a file

s3.delete_object(Bucket=bucket_name, Key=file_key)