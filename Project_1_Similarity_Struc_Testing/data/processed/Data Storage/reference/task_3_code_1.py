`python

import boto3

s3 =boto3 .client ('s3')

bucket_name ='your_bucket_name'

s3 .create_bucket (Bucket =bucket_name )

file_name ='your_file_name'

folder_name ='your_folder_name'

lifecycle_configuration ={

'Rules':[

{

'ID':'Move to Glacier',

'Status':'Enabled',

'Prefix':folder_name ,

'Transitions':[

{

'Days':30 ,

'StorageClass':'GLACIER'

}

]

}

]

}

s3 .put_bucket_lifecycle_configuration (Bucket =bucket_name ,LifecycleConfiguration =lifecycle_configuration )