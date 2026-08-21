import requests
import json
from datetime import datetime ,timedelta
import pandas as pd
import matplotlib .pyplot as plt
import numpy as np
from dateutil .relativedelta import relativedelta

MATOMO_SITE_ID ='YOUR_MATOMO_SITE_ID'
MATOMO_API_KEY ='YOUR_MATOMO_API_KEY'

def initialize_matomo_api ():
    try :
        response =requests .get (f'https://api.matomo.org/index.php?module=API&method=Session.get&format=json&siteId={MATOMO_SITE_ID}&token_auth={MATOMO_API_KEY}&period=day&date=previous30Days')
        return response .json ()
    except Exception as e :
        print (f'Error initializing Matomo API: {e}')

def get_video_views_data ():
    try :
        response =requests .get (f'https://api.matomo.org/index.php?module=API&method=Stats.get&format=json&siteId={MATOMO_SITE_ID}&token_auth={MATOMO_API_KEY}&period=day&date=previous30Days&segment=pageUrl=="/video/*"&category=video')
        return response .json ()
    except Exception as e :
        print (f'Error getting video views data: {e}')

def get_audience_engagement_data ():
    try :
        response =requests .get (f'https://api.matomo.org/index.php?module=API&method=Stats.get&format=json&siteId={MATOMO_SITE_ID}&token_auth={MATOMO_API_KEY}&period=day&date=previous30Days&segment=pageUrl=="/video/*"&category=video')
        return response .json ()
    except Exception as e :
        print (f'Error getting audience engagement data: {e}')

def get_retention_rates_data ():
    try :
        response =requests .get (f'https://api.matomo.org/index.php?module=API&method=Stats.get&format=json&siteId={MATOMO_SITE_ID}&token_auth={MATOMO_API_KEY}&period=day&date=previous30Days&segment=pageUrl=="/video/*"&category=video')
        return response .json ()
    except Exception as e :
        print (f'Error getting retention rates data: {e}')

matomo_api =initialize_matomo_api ()

video_views_data =get_video_views_data ()

audience_engagement_data =get_audience_engagement_data ()

retention_rates_data =get_retention_rates_data ()

video_views_df =pd .DataFrame (video_views_data ['data']['columns'])
video_views_df ['value']=video_views_data ['data']['data']

audience_engagement_df =pd .DataFrame (audience_engagement_data ['data']['columns'])
audience_engagement_df ['value']=audience_engagement_data ['data']['data']

retention_rates_df =pd .DataFrame (retention_rates_data ['data']['columns'])
retention_rates_df ['value']=retention_rates_data ['data']['data']

plt .figure (figsize =(10 ,6 ))
plt .bar (video_views_df ['label'],video_views_df ['value'])
plt .title ('Video Views')
plt .xlabel ('Date')
plt .ylabel ('Views')
plt .show ()

plt .figure (figsize =(10 ,6 ))
plt .bar (audience_engagement_df ['label'],audience_engagement_df ['value'])
plt .title ('Audience Engagement')
plt .xlabel ('Date')
plt .ylabel ('Engagement')
plt .show ()

plt .figure (figsize =(10 ,6 ))
plt .bar (retention_rates_df ['label'],retention_rates_df ['value'])
plt .title ('Retention Rates')
plt .xlabel ('Date')
plt .ylabel ('Retention Rate')
plt .show ()

video_views_df .to_csv ('video_views_data.csv',index =False )

audience_engagement_df .to_csv ('audience_engagement_data.csv',index =False )

retention_rates_df .to_csv ('retention_rates_data.csv',index =False )