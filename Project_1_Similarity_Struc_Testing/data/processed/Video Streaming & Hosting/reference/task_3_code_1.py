`python

from vimeo_api import VimeoOTT

access_token ="your_access_token_here"

account_id ="your_account_id_here"

client =VimeoOTT (access_token )

dashboard =client .create_dashboard (account_id ,name ="Video Analytics Dashboard")

dashboard .add_widget ("video_views",name ="Video Views Widget")

dashboard .add_widget ("audience_engagement",name ="Audience Engagement Widget")

dashboard .add_widget ("retention_rates",name ="Retention Rates Widget")

dashboard .enable_customizable_reports ()

dashboard .save ()