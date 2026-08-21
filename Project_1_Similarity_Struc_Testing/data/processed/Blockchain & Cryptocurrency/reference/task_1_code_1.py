import requests

api_key ="YOUR_API_KEY"

api_secret ="YOUR_API_SECRET"

base_url ="https://api.commerce.coinbase.com/"

headers ={

"X-CC-Api-Key":api_key ,

"X-CC-Version":"2018-03-22",

"Content-Type":"application/json"

}

payload ={

"name":"Example Product",

"description":"Product description",

"local_price":{

"amount":"100.00",

"currency":"USD"

},

"pricing_type":"fixed_price",

"metadata":{

"product_id":"123",

"order_id":"456"

}

}

response =requests .post (base_url +"charges",json =payload ,headers =headers )

print (response .json ())

charge_id ="CHARGE_ID"

response =requests .get (base_url +f"charges/{charge_id}",headers =headers )

print (response .json ())