`python

import boto3

application_name ='your-application-name'

eb_client =boto3 .client ('elasticbeanstalk')

response =eb_client .create_application_version (

ApplicationName =application_name ,

VersionLabel ='v1',

SourceBundle ={

'S3Bucket':'your-s3-bucket-name',

'S3Key':'your-s3-object-key'

}

)

response =eb_client .update_environment (

ApplicationName =application_name ,

EnvironmentName =environment_name ,

VersionLabel ='v1'

)