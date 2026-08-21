`python

# Importing necessary AWS services

import boto3



# Creating an AWS CodePipeline

codepipeline_client = boto3.client('codepipeline')



response = codepipeline_client.create_pipeline(

   pipeline={

       'name': 'MyCI/CDPipeline',

       'roleArn': 'arn:aws:iam::123456789012:role/service-role/AWSCodePipelineServiceRole',

       'stages': [

           {

               'name': 'Source',

               'actions': [

                   {

                       'name': 'SourceAction',

                       'actionTypeId': {

                           'owner': 'AWS',

                           'provider': 'CodeCommit',

                           'version': '1'

                       },

                       'outputArtifacts': [

                           {

                               'name': 'MyApp_Source'

                           }

                       ],

                       'configuration': {

                           'RepositoryName': 'MyAppRepo',

                           'BranchName': 'master'

                       }

                   }

               ]

           },

           {

               'name': 'Build',

               'actions': [

                   {

                       'name': 'BuildAction',

                       'actionTypeId': {

                           'category': 'Build',

                           'owner': 'AWS',

                           'provider': 'CodeBuild',

                           'version': '1'

                       },

                       'inputArtifacts': [

                           {

                               'name': 'MyApp_Source'

                           }

                       ]

                   }

               ]

           },

           {

               'name': 'Staging',

               'actions': [

                   {

                       'name': 'StagingAction',

                       'actionTypeId': {

                           'category': 'Deploy',

                           'owner': 'AWS',

                           'provider': 'CodeDeploy',

                           'version': '1'

                       },

                       'inputArtifacts': [

                           {

                               'name': 'MyApp_Source'

                           }

                       ]

                   }

               ]

           },

           {

               'name': 'Production',

               'actions': [

                   {

                       'name': 'ProductionAction',

                       'actionTypeId': {

                           'category': 'Deploy',

                           'owner': 'AWS',

                           'provider': 'CodeDeploy',

                           'version': '1'

                       },

                       'inputArtifacts': [

                           {

                               'name': 'MyApp_Source'

                           }

                       ]

                   }

               ]

       ]

   }

)