import boto3



# Create CloudFront distribution

cloudfront_client = boto3.client('cloudfront')



distribution_config = {

    'CallerReference': 'your-caller-reference',

    'Aliases': {

        'Quantity': 1,

    },

    'DefaultRootObject': 'index.html',

    'Origins': {

        'Quantity': 1,

            'Id': 'your-origin-id',

            'DomainName': 'your-origin-domain.s3.amazonaws.com',

            'S3OriginConfig': {

                'OriginAccessIdentity': ''

            }

        }]

    },

    'DefaultCacheBehavior': {

        'TargetOriginId': 'your-origin-id',

        'ViewerProtocolPolicy': 'redirect-to-https',

        'ForwardedValues': {

            'QueryString': False,

            'Cookies': {

                'Forward': 'none'

            }

        },

        'MinTTL': 0

    },

    'PriceClass': 'PriceClass_100',

    'Enabled': True

}



response = cloudfront_client.create_distribution(DistributionConfig=distribution_config)



print(response)