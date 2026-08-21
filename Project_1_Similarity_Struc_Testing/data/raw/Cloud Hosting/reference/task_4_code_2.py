`python

# Import necessary AWS services

import boto3



# Create a CodePipeline client

codepipeline_client = boto3.client('codepipeline')

# Define the source and build stages

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



# Create a new CodePipeline

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



# Start the pipeline

response = codepipeline_client.start_pipeline_execution(name='MyPipeline')