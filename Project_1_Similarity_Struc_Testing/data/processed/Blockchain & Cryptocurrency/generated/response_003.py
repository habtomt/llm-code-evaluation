import json
from web3 import Web3
import requests

def connect_to_blockchain ():

    infura_project_id ="YOUR_INFURA_PROJECT_ID"
    w3 =Web3 (Web3 .HTTPProvider (f"https://mainnet.infura.io/v3/{infura_project_id}"))
    return w3

def load_contract (w3 ,contract_address ,contract_abi ):

    contract =w3 .eth .contract (address =contract_address ,abi =contract_abi )
    return contract

def mint_nft (contract ,account ,token_uri ):

    try :

        token_counter =contract .functions .tokenCounter ().call ()

        tx_hash =contract .functions .mintNFT (token_uri ).transact ({"from":account })

        tx_receipt =w3 .eth .wait_for_transaction_receipt (tx_hash )

        new_token_id =token_counter +1

        return new_token_id

    except Exception as e :
        print (f"Error minting NFT: {e}")
        return None

def upload_to_ipfs (file_path ):

    pinata_api_key ="YOUR_PINATA_API_KEY"
    pinata_api_secret ="YOUR_PINATA_API_SECRET"

    url ="https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers ={
    "pinata_api_key":pinata_api_key ,
    "pinata_secret_api_key":pinata_api_secret
    }

    with open (file_path ,"rb")as file :
        file_data =file .read ()

    response =requests .post (url ,headers =headers ,files ={"file":file_data })

    ipfs_hash =response .json ()["IpfsHash"]

    return ipfs_hash

def main ():

    w3 =connect_to_blockchain ()

    contract_address ="YOUR_CONTRACT_ADDRESS"
    contract_abi =json .loads ("YOUR_CONTRACT_ABI")
    contract =load_contract (w3 ,contract_address ,contract_abi )

    account ="YOUR_ACCOUNT_ADDRESS"

    file_path ="path/to/your/media/file"
    ipfs_hash =upload_to_ipfs (file_path )

    token_uri =f"ipfs://{ipfs_hash}"
    new_token_id =mint_nft (contract ,account ,token_uri )

    print (f"New token ID: {new_token_id}")

if __name__ =="__main__":
    main ()