`python

import boto3

region = 'us-west-2'

db_instance_identifier = 'my-database-instance'

username = 'admin'

password = 'mysecretpassword'

client = boto3.client('rds', region_name=region)

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    IAMDatabaseAuthenticationEnabled=True

)

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    StorageEncrypted=True

)

response = client.modify_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    ApplyImmediately=True,

    VpcSecurityGroupIds=[

        'sg-12345678',

    ],

    ApplyImmediately=True

)

response = client.add_role_to_db_instance(

    DBInstanceIdentifier=db_instance_identifier,

    RoleArn='arn:aws:iam::123456789012:role/MyRDSRole'

)

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

    DBInstanceIdentifier=db_instance_identifier

)

print('Database security best practices configured successfully')