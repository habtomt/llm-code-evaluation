import boto3

ecs_client =boto3 .client ('ecs')

task_definition ={
'family':'web-application',
'containerDefinitions':[
{
'name':'web-app-container',
'image':'your-web-application-image-url',
'portMappings':[
{
}
]
}
],
'networkMode':'awsvpc'
}

response =ecs_client .register_task_definition (family =task_definition ['family'],containerDefinitions =task_definition ['containerDefinitions'])

cluster =ecs_client .create_cluster (clusterName ='web-app-cluster')

service_definition ={
'cluster':'web-app-cluster',
'serviceName':'web-app-service',
'taskDefinition':'web-application',
'desiredCount':3 ,
'launchType':'FARGATE',
'networkConfiguration':{
'subnets':['subnet-1234567','subnet-2345678'],
'securityGroups':['sg-12345678'],
'assignPublicIp':'ENABLED'
}
}

ecs_client .create_service (**service_definition )