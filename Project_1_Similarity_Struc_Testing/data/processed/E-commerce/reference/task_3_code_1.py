import flask

from flask import request ,jsonify ,session

from shopify import Shopify

app =flask .Flask (__name__ )

app .secret_key ='super_secret_key'

@app .route ('/register',methods =['POST'])

def register_user ():

    return jsonify ({'message':'User registered successfully'})

@app .route ('/login',methods =['POST'])

def login_user ():

    session ['logged_in']=True

    return jsonify ({'message':'User logged in successfully'})

@app .route ('/profile',methods =['GET','POST'])

def manage_profile ():

    if 'logged_in'in session :

        if request .method =='GET':

            return jsonify ({'message':'User profile retrieved successfully'})

        elif request .method =='POST':

            return jsonify ({'message':'User profile updated successfully'})

    else :

        return jsonify ({'message':'User not logged in'})

    app .run (debug =True )