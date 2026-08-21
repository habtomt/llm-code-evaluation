import boto3

ec2 =boto3 .resource ('ec2')

instance =ec2 .create_instances (

ImageId ='ami-0c55b159cbfafe1f0',

MinCount =1 ,

MaxCount =1 ,

InstanceType ='t2.micro'

)

autoscaling =boto3 .client ('autoscaling')

response =autoscaling .create_auto_scaling_group (

AutoScalingGroupName ='database-scaling-group',

LaunchConfigurationName ='database-launch-config',

MinSize =1 ,

MaxSize =5

)

cloudwatch =boto3 .client ('cloudwatch')

response =cloudwatch .put_metric_alarm (

AlarmName ='database-cpu-utilization',

ComparisonOperator ='GreaterThanThreshold',

EvaluationPeriods =1 ,

MetricName ='CPUUtilization',

Namespace ='AWS/EC2',

Period =60 ,

Statistic ='Average',

Threshold =80.0 ,

ActionsEnabled =True ,

AlarmActions =[

'arn:aws:sns:us-east-1:123456789012:my-topic'

],

Dimensions =[

{

'Name':'InstanceId',

},

]

)