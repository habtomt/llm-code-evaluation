`python

import requests

import matplotlib .pyplot as plt

user_data_response =requests .get ('https://graph.facebook.com/me?access_token=YOUR_ACCESS_TOKEN')

follower_growth_response =requests .get ('https://graph.facebook.com/me/friends?access_token=YOUR_ACCESS_TOKEN')

post_performance_response =requests .get ('https://graph.facebook.com/me/posts?fields=insights.metric(post_impressions,post_engagements)&access_token=YOUR_ACCESS_TOKEN')

plt .figure (figsize =(10 ,5 ))

plt .plot (follower_growth_data_dates ,follower_growth_data_values )

plt .title ('Follower Growth Over Time')

plt .xlabel ('Date')

plt .ylabel ('Number of Followers')

plt .figure (figsize =(10 ,5 ))

plt .bar (post_performance_metrics_labels ,post_performance_metrics_values )

plt .title ('Post Performance Metrics')

plt .xlabel ('Metrics')

plt .ylabel ('Values')

plt .show ()