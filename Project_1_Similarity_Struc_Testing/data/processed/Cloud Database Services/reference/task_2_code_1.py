`python

import boto3

rds = boto3.client('rds', region_name='your_region')

response = rds.create_db_instance(

    AllocatedStorage=20,

    DBInstanceClass='db.t2.micro',

    Engine='mysql',

    MasterUsername='your_master_username',

    MasterUserPassword='your_master_password',

    VpcSecurityGroupIds=['your_security_group_id'],

    BackupRetentionPeriod=7,

    MultiAZ=False,

    StorageType='gp2',

    PubliclyAccessible=False,

    Tags=[

        {

            'Key': 'Name',

            'Value': 'your_db_instance_name'

        },

    ]

)

kms = boto3.client('kms', region_name='your_region')

response = kms.create_key(

    Description='your_key_description',

    KeyUsage='ENCRYPT_DECRYPT'

)

response = rds.modify_db_instance(

    DBInstanceIdentifier='your_db_instance_name',

    StorageEncrypted=True,

    KmsKeyId='your_kms_key_id'

)

response = rds.modify_db_instance(

    DBInstanceIdentifier='your_db_instance_name',

    ApplyImmediately=True,

    VpcSecurityGroupIds=['your_security_group_id'],

    EnableIAMDatabaseAuthentication=True

)

iam = boto3.client('iam', region_name='your_region')

response = iam.create_role(

    RoleName='your_role_name',

    AssumeRolePolicyDocument={

        'Version': '2012-10-17',

        'Statement': [

            {

                'Effect': 'Allow',

                'Principal': {

                    'Service': 'rds.amazonaws.com'

                },

                'Action': 'sts:AssumeRole'

            }

        ]

    }

)

response = iam.put_role_policy(

    RoleName='your_role_name',

    PolicyName='your_policy_name',

    PolicyDocument={

        'Version': '2012-10-17',

        'Statement': [

            {

                'Effect': 'Allow',

                'Action': [

                    'rds:*'

                ],

                'Resource': 'arn:aws:rds:your_region:your_account_id:your_db_instance_name'

            }

    }

)