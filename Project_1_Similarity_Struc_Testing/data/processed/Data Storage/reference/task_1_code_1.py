`python

import boto3

s3 = boto3.client('s3')

bucket_name = 'mylocaldatabase'

s3.create_bucket(Bucket=bucket_name)

buckets = [bucket['Name'] for bucket in response['Buckets']

print('Existing buckets:', buckets)

file_name = 'example.txt'

s3.download_file(bucket_name, file_name, 'downloaded_example.txt')

s3.delete_object(Bucket=bucket_name, Key=file_name)

s3.delete_bucket(Bucket=bucket_name)