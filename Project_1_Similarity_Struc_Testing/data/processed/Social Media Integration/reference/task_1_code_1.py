`python

access_token ='ACCESS_TOKEN'

response =requests .get (graph_api_url ,params ={'access_token':access_token })

data =response .json ()

for post in data ['data']:

    if 'message'in post :

        print ('Message:',post ['message'])

    if 'full_picture'in post :

        print ('Image:',post ['full_picture'])

    if 'source'in post :

        print ('Video:',post ['source'])