`python

import boto3



quicksight = boto3.client('quicksight')



response = quicksight.create_analysis(

    AnalysisId='sales_trend_forecasting',

    Name='Sales Trend Forecasting',

    SourceEntity={

        'SourceTemplate': {

            'DataSetReferences': [

                {

                    'DataSetArn': 'arn:aws:quicksight:us-east-1:123456789012:dataset/sales_data'

                }

            ],

            'Arn': 'arn:aws:quicksight:us-east-1:123456789012:template/sales_trend_template'

        }

    }

)