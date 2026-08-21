import boto3
import os

session =boto3 .Session (
aws_access_key_id ='YOUR_AWS_ACCESS_KEY',
aws_secret_access_key ='YOUR_AWS_SECRET_KEY',
)

cloudfront =session .client ('cloudfront')

distribution_config ={
'CallerReference':'YOUR_CALLER_REFERENCE',
'DefaultRootObject':'index.html',
'Origins':{
'Quantity':1 ,
'Items':[
{
'Id':'YOUR_ORIGIN_ID',
'DomainName':'YOUR_ORIGIN_DOMAIN_NAME',
'CustomHeaders':{
'Quantity':0 ,
},
},
],
},
'DefaultCacheBehavior':{
'ForwardedValues':{
'QueryString':False ,
'Cookies':{
'Forward':'none',
},
},
'TrustedSigners':{
'Enabled':False ,
'Quantity':0 ,
},
'ViewerProtocolPolicy':'allow-all',
'MinTTL':0 ,
},
'CacheBehaviors':{
'Quantity':0 ,
},
}

def create_distribution ():
    try :
        response =cloudfront .create_distribution (DistributionConfig =distribution_config )
        print (response )
    except Exception as e :
        print (e )

def update_distribution (distribution_id ):
    try :
        response =cloudfront .update_distribution (
        DistributionConfig =distribution_config ,
        Id =distribution_id ,
        )
        print (response )
    except Exception as e :
        print (e )

def get_distribution (distribution_id ):
    try :
        response =cloudfront .get_distribution (Id =distribution_id )
        print (response )
    except Exception as e :
        print (e )

def list_distributions ():
    try :
        response =cloudfront .list_distributions ()
        print (response )
    except Exception as e :
        print (e )

if __name__ =='__main__':
    create_distribution ()