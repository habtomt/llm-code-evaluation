`python

import boto3

client =boto3 .client ('rds')

response =client .modify_db_instance (

DBInstanceIdentifier ='your-db-instance-id',

PerformanceInsightsKMSKeyId ='your-kms-key-id',

PerformanceInsightsRetentionPeriod =7 ,

)

cloudwatch =boto3 .client ('cloudwatch')

for metric in ['CPUUtilization','FreeableMemory','QueryThroughput','FreeStorageSpace']:

    alarm_name =f'{metric}HighUtilizationAlarm'

    response =cloudwatch .put_metric_alarm (

    AlarmName =alarm_name ,

    AlarmDescription =f'Alarm for high {metric} utilization',

    ActionsEnabled =True ,

    MetricName =metric ,

    Namespace ='AWS/RDS',

    Statistic ='Average',

    Dimensions =[{

    'Name':'DBInstanceIdentifier',

    'Value':'your-db-instance-id'

    }],

    Period =300 ,

    EvaluationPeriods =1 ,

    Threshold =80.0 ,

    ComparisonOperator ='GreaterThanThreshold',

    )

for metric in ['CPUUtilization','FreeableMemory','QueryThroughput','FreeStorageSpace']:

    response =cloudwatch .put_anomaly_detector (

    Namespace ='AWS/RDS',

    MetricName =metric ,

    Dimensions =[{

    'Name':'DBInstanceIdentifier',

    'Value':'your-db-instance-id'

    }],

    Stat ='Average'

    )