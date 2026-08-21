`python

import boto3



# Create an Elastic Beanstalk application

elasticbeanstalk = boto3.client('elasticbeanstalk')

response = elasticbeanstalk.create_application(

    ApplicationName='WordPressApp',

    Description='WordPress application'

)



# Create an environment for the application

response = elasticbeanstalk.create_environment(

    ApplicationName='WordPressApp',

    EnvironmentName='WordPressEnvironment',

    SolutionStackName='64bit Amazon Linux 2 v5.3.1 running PHP 7.4',

    OptionSettings=[

        {

            'Namespace': 'aws:autoscaling:launchconfiguration',

            'OptionName': 'EC2KeyName',

            'Value': 'your-key-pair'

        },

            'Namespace': 'aws:autoscaling:launchconfiguration',

            'OptionName': 'InstanceType',

            'Value': 't2.micro'

        },

        {

            'Namespace': 'aws:elasticbeanstalk:environment:process:default',

            'OptionName': 'DocumentRoot',

            'Value': '/public'

        },

        {

            'Namespace': 'aws:elasticbeanstalk:container:php:phpini',

            'OptionName': 'document_root',

            'Value': '/public'

        },

        {

            'Namespace': 'aws:elasticbeanstalk:container:php:phpini',

            'OptionName': 'allow_url_fopen',

            'Value': 'On'

        }

    ]

)



# Create an RDS database for WordPress data

rds = boto3.client('rds')

response = rds.create_db_instance(

    DBInstanceIdentifier='wordpress-db',

    AllocatedStorage=20,

    Engine='mysql',

    MasterUsername='admin',

    MasterUserPassword='your-password',

    DBInstanceClass='db.t2.micro'

)



# Wait for the RDS instance to be available

waiter = rds.get_waiter('db_instance_available')

waiter.wait(DBInstanceIdentifier='wordpress-db')