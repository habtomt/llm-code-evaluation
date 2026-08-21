from flask import Flask ,request ,jsonify
from flask_jwt_extended import JWTManager ,jwt_required ,create_access_token ,get_jwt_identity
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson .objectid import ObjectId
import os

app =Flask (__name__ )

app .config ['JWT_SECRET_KEY']='YOUR_SECRET_KEY'
jwt =JWTManager (app )

bcrypt =Bcrypt (app )

client =MongoClient ('mongodb://localhost:27017/')
db =client ['userAuth']
users_collection =db ['users']

def hash_password (password ):
    return bcrypt .generate_password_hash (password ).decode ('utf-8')

def compare_password (password ,hashed_password ):
    return bcrypt .check_password_hash (hashed_password ,password )

@app .route ('/register',methods =['POST'])
def register ():
    try :

        username =request .json ['username']
        password =request .json ['password']

        if users_collection .find_one ({'username':username }):
            return jsonify ({'error':'Username already exists'}),400

        hashed_password =hash_password (password )

        user ={
        'username':username ,
        'password':hashed_password
        }

        users_collection .insert_one (user )

        return jsonify ({'message':'User created'}),201
    except Exception as e :

        return jsonify ({'error':str (e )}),500

@app .route ('/login',methods =['POST'])
def login ():
    try :

        username =request .json ['username']
        password =request .json ['password']

        user =users_collection .find_one ({'username':username })

        if not user :
            return jsonify ({'error':'Invalid credentials'}),401

        if not compare_password (password ,user ['password']):
            return jsonify ({'error':'Invalid credentials'}),401

        access_token =create_access_token (identity =str (user ['_id']))

        return jsonify ({'access_token':access_token }),200
    except Exception as e :

        return jsonify ({'error':str (e )}),500

@app .route ('/profile',methods =['GET'])
@jwt_required
def profile ():
    try :

        user_id =get_jwt_identity ()

        user =users_collection .find_one ({'_id':ObjectId (user_id )})

        if not user :
            return jsonify ({'error':'User not found'}),404

        return jsonify ({'username':user ['username']}),200
    except Exception as e :

        return jsonify ({'error':str (e )}),500

if __name__ =='__main__':
    app .run (debug =True )