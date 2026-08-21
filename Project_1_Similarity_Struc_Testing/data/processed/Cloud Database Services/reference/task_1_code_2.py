`python

import boto3

client =boto3 .client ('rds')

db_identifier ='my-rds-instance'

min_instances =1

max_instances =5

scaling_policy ={

'ResourceID':'my-rds-instance',

'ServiceNamespace':'rds',

'PolicyName':'rds-cpu-utilization-scaling',

'PolicyType':'TargetTrackingScaling',

'TargetTrackingScalingPolicyConfiguration':{

'TargetValue':70.0 ,

'PredefinedMetricSpecification':{

'PredefinedMetricType':'RDSReaderAverageCPUUtilization'

},

'ScaleOutCooldown':60 ,

'ScaleInCooldown':60

}

}

response =client .register_scalable_target (

ServiceNamespace ='rds',

MaxCapacity =max_instances ,

MinCapacity =min_instances ,

ResourceId =db_identifier ,

ScalableDimension ='rds:cluster:write-operations:count'

)

response =client .put_scaling_policy (

PolicyName =scaling_policy ['PolicyName'],

ServiceNamespace =scaling_policy ['ServiceNamespace'],

ResourceId =scaling_policy ['ResourceID'],

ScalableDimension =scaling_policy ['ScalableDimension'],

PolicyType =scaling_policy ['PolicyType'],

)