import boto3

eb_client =boto3 .client ('elasticbeanstalk')

app_create_response =eb_client .create_application (

ApplicationName ='StaticWebsiteApp',

Description ='Application for hosting static website'

)

env_create_response =eb_client .create_environment (

ApplicationName ='StaticWebsiteApp',

EnvironmentName ='StaticWebsiteEnv',

SolutionStackName ='64bit Amazon Linux 2 v3.2.4 running Python 3.7',

OptionSettings =[

{

'Namespace':'aws:elasticbeanstalk:environment',

'OptionName':'EnvironmentType',

'Value':'LoadBalanced'

},

]

)

eb_client .create_source_bundle (

ApplicationName ='StaticWebsiteApp',

SourceBundle ={

'S3Bucket':'your-s3-bucket-name',

'S3Key':'your-s3-key'

}

)

eb_client .update_environment (

ApplicationName ='StaticWebsiteApp',

EnvironmentName ='StaticWebsiteEnv',

OptionSettings =[

{

'Namespace':'aws:elasticbeanstalk:environment',

'OptionName':'StaticFiles',

'Value':'/public'

},

]

)