import boto3

quicksight =boto3 .client ('quicksight')

dataset_response =quicksight .create_data_set (
AwsAccountId ='your_aws_account_id',
DataSetId ='customer_dataset',
Name ='CustomerDataset',
PhysicalTableMap ={
'customerData':{
'CustomSql':{
'DataSourceArn':'arn:aws:quicksight:region:your_aws_account_id:datasource/datasource_id',
'Name':'customer_data_query',
'SqlQuery':'SELECT * FROM customer_table'
}
}
},
LogicalTableMap ={
'customerData':{
'Alias':'CustomerData',
'Source':{
'PhysicalTableId':'customerData'
}
}
},
ImportMode ='SPICE'
)

analysis_response =quicksight .create_analysis (
AwsAccountId ='your_aws_account_id',
AnalysisId ='customer_segmentation_analysis',
Name ='CustomerSegmentationAnalysis',
SourceEntity ={
'SourceTemplate':{
'DataSetReferences':[
{
'DataSetPlaceholder':'customerDatasetPlaceholder',
'DataSetArn':'arn:aws:quicksight:region:your_aws_account_id:dataset/customer_dataset'
}
],
'Arn':'arn:aws:quicksight:region:your_aws_account_id:template/customer_segmentation_template'
}
}
)

dashboard_response =quicksight .create_dashboard (
AwsAccountId ='your_aws_account_id',
DashboardId ='customer_segmentation_dashboard',
Name ='CustomerSegmentationDashboard',
SourceEntity ={
'SourceTemplate':{
'DataSetReferences':[
{
'DataSetPlaceholder':'customerDatasetPlaceholder',
'DataSetArn':'arn:aws:quicksight:region:your_aws_account_id:dataset/customer_dataset'
}
],
'Arn':'arn:aws:quicksight:region:your_aws_account_id:template/customer_segmentation_dashboard_template'
}
}
)