`python

import boto3



s3 = boto3.client('s3')



# Create a bucket

bucket_name = 'my-archived-bucket'

s3.create_bucket(Bucket=bucket_name)



lifecycle_configuration = {

    'Rules': [

        {

            'ID': 'ArchiveRule',

            'Filter': {

                'Prefix': ''

            },

            'Status': 'Enabled',

            'Transitions': [

                {

                    'Days': 30,

                    'StorageClass': 'STANDARD_IA'

                },

                {

                    'Days': 365,

                }

            ],

            'Expiration': {

                'Days': 3650

            }

        }

    ]

}

s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_configuration)