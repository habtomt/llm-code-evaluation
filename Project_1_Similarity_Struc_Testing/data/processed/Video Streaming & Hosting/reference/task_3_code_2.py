`python

import requests

url ='https://api.vimeo.com/path/to/analytics'

access_token ='your_access_token_here'

headers ={

'Authorization':'Bearer '+access_token ,

'Content-Type':'application/json'

}

response =requests .get (url ,headers =headers )

if response .status_code ==200 :

    data =response .json ()

else :