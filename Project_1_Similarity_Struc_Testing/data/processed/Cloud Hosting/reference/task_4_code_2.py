`python

import boto3

codepipeline_client = boto3.client('codepipeline')

source_stage = {

    'name': 'Source',

    'actions': [

        {

            'name': 'Source',

            'actionTypeId': {

                'category': 'Source',

                'owner': 'AWS',

                'version': '1',

                'provider': 'GitHub'

            },

            'runOrder': 1,

            'configuration': {

                'Owner': 'myGitHubOwner',

                'Repo': 'myGitHubRepo',

                'Branch': 'master',

                'OAuthToken': 'myGitHubOAuthToken'

            },

            'outputArtifacts': [

                    'name': 'SourceOutput'

                }

            ]

        }

    ]

}

build_stage = {

    'name': 'Build',

    'actions': [

        {

            'name': 'Build',

            'actionTypeId': {

                'category': 'Build',

                'owner': 'AWS',

                'version': '1',

                'provider': 'CodeBuild'

            },

            'runOrder': 1,

            'configuration': {

                'ProjectName': 'myCodeBuildProject'

            },

            'inputArtifacts': [

                {

                    'name': 'SourceOutput'

                }

            ],

            'outputArtifacts': [

                {

                    'name': 'BuildOutput'

                }

            ]

        }

    ]

}

response = codepipeline_client.create_pipeline(

    pipeline={

        'name': 'MyPipeline',

        'roleArn': 'arn:aws:iam::123456789012:role/MyCodePipelineRole',

        'stages': [source_stage, build_stage],

        'artifactStore': {

            'type': 'S3',

            'location': 'myPipelineArtifactBucket'

        }

    }

)

response = codepipeline_client.start_pipeline_execution(name='MyPipeline')