`python

import boto3

# Create S3 client

s3 = boto3.client('s3')



# Create bucket

bucket_name = 'your_bucket_name'

s3.create_bucket(Bucket=bucket_name)



# Upload a file

file_name = 'your_file_name'

folder_name = 'your_folder_name'



# Set lifecycle policy to transition objects to Glacier storage class

lifecycle_configuration = {

    'Rules': [

        {

            'ID': 'Move to Glacier',

            'Status': 'Enabled',

            'Prefix': folder_name,

            'Transitions': [

                {

                    'Days': 30,

                    'StorageClass': 'GLACIER'

                }

            ]

        }

    ]

}



s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_configuration)