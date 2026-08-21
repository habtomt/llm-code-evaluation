import boto3

ecs =boto3 .client ('ecs')

ec2 =boto3 .resource ('ec2')

instance =ec2 .create_instances (

MinCount =1 ,

MaxCount =1 ,

InstanceType ='t2.micro'

)

cluster =ecs .create_cluster (

clusterName ='web-cluster'

)

task_definition =ecs .register_task_definition (

family ='web-app',

networkMode ='bridge',

containerDefinitions =[

{

'name':'web-container',

'image':'web-app-image:latest',

'cpu':256 ,

'memory':512 ,

'portMappings':[

{

'containerPort':80 ,

'hostPort':80

}

]

}

]

)

service =ecs .create_service (

cluster ='web-cluster',

serviceName ='web-service',

taskDefinition ='web-app',

desiredCount =2

)