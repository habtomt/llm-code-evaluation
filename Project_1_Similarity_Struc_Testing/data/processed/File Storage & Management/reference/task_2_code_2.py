import requests

import json

base_url ="https://api.box.com/2.0/"

def create_access_management_system (user_id ,role ,permissions ):

    headers ={"Authorization":f"Bearer {auth_token}","Content-Type":"application/json"}

    access_payload ={

    "type":"user",

    "id":user_id ,

    "role":role ,

    "can_edit":permissions ["can_edit"],

    "can_view":permissions ["can_view"]

    }

    access_url =f"{base_url}access"

    response =requests .post (access_url ,headers =headers ,data =json .dumps (access_payload ))

    if response .status_code ==201 :

        print ("User access and permissions created successfully")

    else :

        print (f"Failed to create user access: {response.text}")

user_id ="12345"

role ="editor"

permissions ={"can_edit":True ,"can_view":True }

create_access_management_system (user_id ,role ,permissions )