`python

import boto3



def create_cloudfront_distribution(bucket_name):

    client = boto3.client('cloudfront')

    caller_reference = 'cdn-setup-example'

    default_cache_behavior = {

        'TargetOriginId': f'S3-{bucket_name}',

        'ForwardedValues': {

            'QueryString': False

        },

        'ViewerProtocolPolicy': 'redirect-to-https'

    }

    distribution_config = {

        'CallerReference': caller_reference,

        'Comment': 'CDN for static assets',

        'DefaultCacheBehavior': default_cache_behavior,

        'Origins': {

            'Quantity': 1,

            'Items': [

                {

                    'DomainName': f'{bucket_name}.s3.amazonaws.com',

                    'S3OriginConfig': {

                        'OriginAccessIdentity': ''

                    }

                }

            ]

        },

        'Enabled': True

    }

    response = client.create_distribution(DistributionConfig=distribution_config)

    distribution_id = response['Distribution']['Id']

    return distribution_id



distribution_id = create_cloudfront_distribution(bucket_name)

print(f'CloudFront distribution created with ID: {distribution_id}')