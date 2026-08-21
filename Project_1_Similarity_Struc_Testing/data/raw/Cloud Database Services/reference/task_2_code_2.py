`python

import boto3



# Set up AWS credentials and region

region = 'us-west-2'

db_instance_identifier = 'my-database-instance'

username = 'admin'

password = 'mysecretpassword'



# Create a RDS client

client = boto3.client('rds', region_name=region)



# Enable IAM database authentication

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    IAMDatabaseAuthenticationEnabled=True

)



# Enable encryption at rest

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    StorageEncrypted=True

)



# Enable encryption for data in transit

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    VpcSecurityGroupIds=[

        'sg-12345678',  # Replace with your VPC security group ID

    ],

    ApplyImmediately=True

)



# Set up role-based access controls

# Assign IAM role to the database instance

response = client.add_role_to_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    RoleArn='arn:aws:iam::123456789012:role/MyRDSRole'

)



# Set up audit logging

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    EnableAuditLog=True,

    AuditDestinations=[

        {

            'S3BucketName': 'my-audit-logs-bucket',

            'KMSMasterKeyArn': 'arn:aws:kms:us-west-2:123456789012:key/abcd1234-12ab-34cd-56ef-1234567890ab'

        }

    ]

)



# Restart the database instance to apply the changes

    DBInstanceIdentifier=db_instance_identifier

)



print('Database security best practices configured successfully')