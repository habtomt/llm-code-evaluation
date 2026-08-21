import boto3

import os

import subprocess



# Define AWS credentials

AWS_ACCESS_KEY_ID = 'your_access_key_id'

AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

AWS_DEFAULT_REGION = 'your_default_region'



s3 = boto3.client('s3',

                  aws_access_key_id=AWS_ACCESS_KEY_ID,

                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

                  region_name=AWS_DEFAULT_REGION)



# Define the directory to backup

backup_directory = '/path/to/your/data'



# Define the S3 bucket to store backups

s3_bucket_name = 'your-s3-bucket-name'



# Backup script using tar

backup_command = 'tar -czf backup.tar.gz {}'.format(backup_directory)

subprocess.run(backup_command, shell=True)



# Upload backup to S3

s3.upload_file('backup.tar.gz', s3_bucket_name, 'backup.tar.gz')



# Check if the backup upload was successful

response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix='backup.tar.gz')

if 'Contents' in response:

    print('Backup uploaded successfully')

else:

    print('Backup upload failed')