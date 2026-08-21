import boto3

ec2 =boto3 .resource ('ec2')

client =boto3 .client ('ec2')

instance =ec2 .create_instances (

ImageId ='ami-0c55b159cbfafe1f0',

MinCount =1 ,

MaxCount =1 ,

InstanceType ='t2.micro',

)