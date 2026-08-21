import boto3

quicksight =boto3 .client ('quicksight',region_name ='us-east-1')

response =quicksight .create_analysis (
AwsAccountId ='123456789012',
AnalysisId ='customer_segmentation_analysis',
Name ='Customer Segmentation Analysis',
SourceEntity ={
'SourceTemplate':{
'DataSetReferences':[
{
'DataSetPlaceholder':'CustomerDataSet',
'DataSetArn':'arn:aws:quicksight:us-east-1:123456789012:dataset/CustomerDataSet'
}
],
'Arn':'arn:aws:quicksight:::template/prod/SuperCoolTemplate'
}
},
Permissions =[
{
'Principal':'arn:aws:quicksight:us-east-1:123456789012:group/default',
'Actions':[
'quicksight:DescribeAnalysisPermissions',
'quicksight:Query',
'quicksight:UpdateAnalysis',
'quicksight:DeleteAnalysis',
'quicksight:UpdateAnalysisPermissions'
]
}
]
)

response =quicksight .create_data_set (
AwsAccountId ='123456789012',
DataSetId ='customer_segmentation_dataset',
Name ='Customer Segmentation Dataset',
PhysicalTableMap ={
'CustomerDataSet':{
'CustomSql':{
'DataSourceArn':'arn:aws:quicksight:us-east-1:123456789012:data-source/MyAthenaDataSource',
'Name':'CustomerDataSet',
'SqlQuery':'SELECT * FROM customer_data'
}
}
},
LogicalTableMap ={
'CustomerDataSet':{
'Alias':'CustomerDataSet',
'Source':{
'JoinInstruction':{
'OnClause':'CustomerDataSet.CustomerId = TransactionDataSet.CustomerId',
'Type':'INNER',
'LeftOperand':'CustomerDataSet',
'RightOperand':'TransactionDataSet'
}
}
}
},
ImportMode ='SPICE'
)

dashboard_response =quicksight .create_dashboard (
AwsAccountId ='123456789012',
DashboardId ='customer_segmentation_dashboard',
Name ='Customer Segmentation Dashboard',
SourceEntity ={
'SourceTemplate':{
'DataSetReferences':[
{
'DataSetPlaceholder':'CustomerSegmentationDataSet',
'DataSetArn':'arn:aws:quicksight:us-east-1:123456789012:dataset/CustomerSegmentationDataSet'
}
],
'Arn':'arn:aws:quicksight:us-east-1:123456789012:template/CustomerSegmentationTemplate'
}
}
)