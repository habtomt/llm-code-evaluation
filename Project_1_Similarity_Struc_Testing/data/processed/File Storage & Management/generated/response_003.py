from cryptography .hazmat .primitives .ciphers import Cipher ,algorithms ,modes
from cryptography .hazmat .backends import default_backend
from cryptography .hazmat .primitives import padding
from cryptography .hazmat .primitives .kdf .pbkdf2 import PBKDF2HMAC
from cryptography .hazmat .primitives import hashes
import os
import base64
import requests
import getpass

KEY_SIZE =32
BLOCK_SIZE =128
IV_SIZE =16

def generate_key (password :str ,salt :bytes )->bytes :

    kdf =PBKDF2HMAC (
    algorithm =hashes .SHA256 (),
    length =KEY_SIZE ,
    salt =salt ,
    iterations =100000 ,
    backend =default_backend ()
    )
    return kdf .derive (password .encode ())

def encrypt_file (file_path :str ,password :str )->None :
    try :

        with open (file_path ,'rb')as f :
            plaintext =f .read ()

        salt =os .urandom (16 )
        iv =os .urandom (IV_SIZE )

        key =generate_key (password ,salt )

        padder =padding .PKCS7 (BLOCK_SIZE ).padder ()
        padded_data =padder .update (plaintext )+padder .finalize ()

        cipher =Cipher (algorithms .AES (key ),modes .CBC (iv ),backend =default_backend ())
        encryptor =cipher .encryptor ()
        ciphertext =encryptor .update (padded_data )+encryptor .finalize ()

        with open (file_path +'.enc','wb')as f :
            f .write (salt +iv +ciphertext )
        print ("File encrypted successfully.")
    except Exception as e :
        print (f"Error encrypting file: {e}")

def decrypt_file (file_path :str ,password :str )->None :
    try :

        with open (file_path ,'rb')as f :
            encrypted_data =f .read ()

        salt =encrypted_data [:16 ]
        iv =encrypted_data [16 :32 ]
        ciphertext =encrypted_data [32 :]

        key =generate_key (password ,salt )

        cipher =Cipher (algorithms .AES (key ),modes .CBC (iv ),backend =default_backend ())
        decryptor =cipher .decryptor ()
        padded_data =decryptor .update (ciphertext )+decryptor .finalize ()

        unpadder =padding .PKCS7 (BLOCK_SIZE ).unpadder ()
        plaintext =unpadder .update (padded_data )+unpadder .finalize ()

        with open (file_path [:-4 ]+'.dec','wb')as f :
            f .write (plaintext )
        print ("File decrypted successfully.")
    except Exception as e :
        print (f"Error decrypting file: {e}")

def transfer_encrypted_file (url :str ,file_path :str )->None :
    try :

        with open (file_path ,'rb')as f :
            file_data =f .read ()
            response =requests .post (url ,data =file_data ,verify =True )
        if response .status_code ==200 :
            print ("File transferred successfully.")
        else :
            print ("Failed to transfer file.")
    except Exception as e :
        print (f"Error transferring file: {e}")

def main ():
    file_path =input ("Enter the file path: ")
    password =getpass .getpass ("Enter the password: ")
    action =input ("Enter the action (encrypt/decrypt/transfer): ")

    if action =="encrypt":
        encrypt_file (file_path ,password )
    elif action =="decrypt":
        decrypt_file (file_path ,password )
    elif action =="transfer":
        url =input ("Enter the URL: ")
        transfer_encrypted_file (url ,file_path )
    else :
        print ("Invalid action.")

if __name__ =="__main__":
    main ()