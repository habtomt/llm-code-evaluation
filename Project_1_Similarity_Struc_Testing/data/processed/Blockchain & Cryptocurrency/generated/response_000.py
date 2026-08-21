from web3 import Web3
import json
import os
from cryptography .fernet import Fernet

def setup_ethereum_node (api_key ):

    provider =Web3 .HTTPProvider (f'https://mainnet.infura.io/v3/{api_key}')
    web3 =Web3 (provider )
    return web3

def create_wallet (web3 ):

    account =web3 .eth .account .create ()
    return {
    'address':account .address ,
    'private_key':account .private_key .hex ()
    }

def get_balance (web3 ,address ):

    balance =web3 .eth .get_balance (address )
    return web3 .fromWei (balance ,'ether')

def send_transaction (web3 ,sender_private_key ,to_address ,amount ):

    sender_account =web3 .eth .account .from_key (sender_private_key )
    nonce =web3 .eth .getTransactionCount (sender_account .address )
    tx ={
    'nonce':nonce ,
    'to':to_address ,
    'value':web3 .toWei (amount ,'ether'),
    'gas':21000 ,
    'gasPrice':web3 .toWei ('50','gwei')
    }

    signed_tx =web3 .eth .account .sign_transaction (tx ,sender_private_key )
    tx_hash =web3 .eth .sendRawTransaction (signed_tx .rawTransaction )
    return tx_hash .hex ()

def encrypt_private_key (private_key ):

    key =Fernet .generate_key ()
    cipher_suite =Fernet (key )
    cipher_text =cipher_suite .encrypt (private_key .encode ())
    return key ,cipher_text

def decrypt_private_key (key ,cipher_text ):

    cipher_suite =Fernet (key )
    plain_text =cipher_suite .decrypt (cipher_text )
    return plain_text .decode ()

if __name__ =="__main__":

    api_key ='YOUR_INFURA_API_KEY'
    web3 =setup_ethereum_node (api_key )

    wallet =create_wallet (web3 )
    print (f"New Wallet Address: {wallet['address']}")

    balance =get_balance (web3 ,wallet ['address'])
    print (f"Balance: {balance} ETH")

    key ,cipher_text =encrypt_private_key (wallet ['private_key'])
    print (f"Encrypted Private Key: {cipher_text}")

    decrypted_private_key =decrypt_private_key (key ,cipher_text )
    print (f"Decrypted Private Key: {decrypted_private_key}")

    try :

        pass
    except Exception as e :
        print (f"Error sending transaction: {e}")