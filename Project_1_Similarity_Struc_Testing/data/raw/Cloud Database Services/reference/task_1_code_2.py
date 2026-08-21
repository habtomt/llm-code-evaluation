`python

import boto3



# Connect to the Amazon RDS client

client = boto3.client('rds')



# Define the RDS DB identifier and the minimum and maximum instance count

db_identifier = 'my-rds-instance'

min_instances = 1

max_instances = 5



# Define the scaling policy to scale based on CPU utilization

scaling_policy = {

    'ResourceID': 'my-rds-instance',

    'ServiceNamespace': 'rds',

    'PolicyName': 'rds-cpu-utilization-scaling',

    'PolicyType': 'TargetTrackingScaling',

    'TargetTrackingScalingPolicyConfiguration': {

        'TargetValue': 70.0,

        'PredefinedMetricSpecification': {

            'PredefinedMetricType': 'RDSReaderAverageCPUUtilization'

        },

        'ScaleOutCooldown': 60,

        'ScaleInCooldown': 60

    }

}



# Register the scaling policy

response = client.register_scalable_target(

    ServiceNamespace='rds',

    MaxCapacity=max_instances,

    MinCapacity=min_instances,

    ResourceId=db_identifier,

    ScalableDimension='rds:cluster:write-operations:count'

)



# Create the scaling policy

response = client.put_scaling_policy(

    PolicyName=scaling_policy['PolicyName'],

    ServiceNamespace=scaling_policy['ServiceNamespace'],

    ResourceId=scaling_policy['ResourceID'],

    ScalableDimension=scaling_policy['ScalableDimension'],

    PolicyType=scaling_policy['PolicyType'],

)