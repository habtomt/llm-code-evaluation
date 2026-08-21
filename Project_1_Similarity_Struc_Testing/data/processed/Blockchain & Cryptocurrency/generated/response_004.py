import hashlib
import json
from flask import Flask ,request ,jsonify
from pymongo import MongoClient
from web3 import Web3
import os

app =Flask (__name__ )

client =MongoClient ('mongodb://localhost:27017/')
db =client ['identity_verification']
collection =db ['identities']

w3 =Web3 (Web3 .HTTPProvider ('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

contract_address ='YOUR_CONTRACT_ADDRESS'
contract_abi =json .loads ('YOUR_CONTRACT_ABI')

contract =w3 .eth .contract (address =contract_address ,abi =contract_abi )

def register_identity (identity_attributes ):

    hashed_attributes =hashlib .sha256 (json .dumps (identity_attributes ).encode ()).hexdigest ()

    identity ={
    'attributes':identity_attributes ,
    'hashed_attributes':hashed_attributes ,
    'is_verified':False
    }

    collection .insert_one (identity )

    tx_hash =contract .functions .registerIdentity (hashed_attributes ).transact ()

    return tx_hash

def verify_identity (address ):

    identity =collection .find_one ({'address':address })

    if identity :
        collection .update_one ({'address':address },{'$set':{'is_verified':True }})

        tx_hash =contract .functions .verifyIdentity (address ).transact ()

        return tx_hash
    else :
        return None

@app .route ('/register',methods =['POST'])
def register ():
    identity_attributes =request .get_json ()
    tx_hash =register_identity (identity_attributes )
    return jsonify ({'tx_hash':tx_hash })

@app .route ('/verify',methods =['POST'])
def verify ():
    address =request .get_json ()['address']
    tx_hash =verify_identity (address )
    return jsonify ({'tx_hash':tx_hash })

if __name__ =='__main__':
    app .run (debug =True )