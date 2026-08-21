`python

import boto3



elasticbeanstalk = boto3.client('elasticbeanstalk')

response = elasticbeanstalk.create_application(

    ApplicationName='WordPressSite',

    Description='Application for hosting WordPress site'

)



# Create a new environment

response = elasticbeanstalk.create_environment(

    EnvironmentName='WordPressEnvironment',

    SolutionStackName='64bit Amazon Linux 2018.03 v2.9.11 running PHP 7.2',

    OptionSettings=[

        {

            'Namespace': 'aws:autoscaling:launchconfiguration',

            'OptionName': 'IamInstanceProfile',

            'Value': 'aws-elasticbeanstalk-ec2-role'

        },

        {

            'Namespace': 'aws:autoscaling:launchconfiguration',

            'OptionName': 'InstanceType',

            'Value': 't2.micro'

        }

    ]

)