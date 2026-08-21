`python

import boto3



rds = boto3.client('rds')



db_instance_identifier = 'your-db-instance-identifier'



cloudwatch = boto3.client('cloudwatch')



def create_cloudwatch_alarm(metric_name, comparison_operator, threshold, period, evaluation_periods):

    response = cloudwatch.put_metric_alarm(

        AlarmName=f'{db_instance_identifier}_{metric_name}_alarm',

        AlarmDescription=f'Alarm for {metric_name} on RDS instance {db_instance_identifier}',

        ActionsEnabled=True,

        AlarmActions=[

            'your-SNS-topic-arn'

        ],

        MetricName=metric_name,

        Namespace='AWS/RDS',

        Statistic='Average',

        Dimensions=[

                'Name': 'DBInstanceIdentifier',

                'Value': db_instance_identifier

            },

        ],

        Period=period,

        EvaluationPeriods=evaluation_periods,

        Threshold=threshold,

    )

    print(response)



create_cloudwatch_alarm('CPUUtilization', 'GreaterThanThreshold', 80, 300, 2)

create_cloudwatch_alarm('FreeableMemory', 'LessThanThreshold', 20, 300, 2)

create_cloudwatch_alarm('WriteIOPS', 'GreaterThanThreshold', 1000, 300, 2)

create_cloudwatch_alarm('ReadIOPS', 'GreaterThanThreshold', 1000, 300, 2)

create_cloudwatch_alarm('DatabaseConnections', 'GreaterThanThreshold', 500, 300, 2)

create_cloudwatch_alarm('FreeStorageSpace', 'LessThanThreshold', 2048, 300, 2)