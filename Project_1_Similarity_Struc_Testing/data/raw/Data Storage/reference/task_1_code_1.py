`python

import boto3



# Create an S3 client

s3 = boto3.client('s3')



# Create a new bucket

bucket_name = 'mylocaldatabase'

s3.create_bucket(Bucket=bucket_name)



# List all buckets

buckets = [bucket['Name'] for bucket in response['Buckets']

print('Existing buckets:', buckets)



# Upload a file to the bucket

file_name = 'example.txt'



# Download a file from the bucket

s3.download_file(bucket_name, file_name, 'downloaded_example.txt')



# Delete an object from the bucket

s3.delete_object(Bucket=bucket_name, Key=file_name)



# Delete the bucket

s3.delete_bucket(Bucket=bucket_name)