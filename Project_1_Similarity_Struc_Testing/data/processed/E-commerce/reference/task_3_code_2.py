import flask

import requests

import json

@app .route ('/register',methods =['POST'])

def user_registration ():

    user_data =flask .request .json

    response =requests .post ('https://api.shopify.com/users/register',json =user_data )

    return response .json (),response .status_code

@app .route ('/login',methods =['POST'])

def user_login ():

    user_credentials =flask .request .json

    response =requests .post ('https://api.shopify.com/users/login',json =user_credentials )

    if response .status_code ==200 :

        flask .session ['user_id']=response .json ()['user_id']

    return response .json (),response .status_code

@app .route ('/profile',methods =['GET','PUT'])

def manage_profile ():

    if 'user_id'in flask .session :

        user_id =flask .session ['user_id']

        if flask .request .method =='GET':

            response =requests .get (f'https://api.shopify.com/users/{user_id}/profile')

        elif flask .request .method =='PUT':

            new_profile_data =flask .request .json

            response =requests .put (f'https://api.shopify.com/users/{user_id}/profile',json =new_profile_data )

        return response .json (),response .status_code

    else :

        return 'Unauthorized',401

if __name__ =='__main__':

    app .secret_key ='super_secret_key'

    app .run ()