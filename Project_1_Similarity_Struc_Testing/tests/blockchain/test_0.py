import os
import sys
import ast
from pathlib import Path
import pytest

# root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# ntw gags
os.environ["WEB3_PROVIDER_URI"] = "http://127.0.0.1:8545" 
os.environ["INFURA_URL"] = "http://127.0.0.1:8545"
os.environ["PRIVATE_KEY"] = "dummy_private_key_for_testing"

APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    pass

def get_source_code():
    #read application source code for structural analysis
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def test_wallet_creation():
    #""rRequirement is to develop a system creating digital wallets
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization  "
    
    source = get_source_code().lower()
    
    # llook for custom wallet
    has_wallet_class = "class wallet" in source or "class account" in source
    
    #Look for cryptographic key generation
    has_key_generation = any(keyword in source for keyword in ["generate_key", "private_key", "public_key", "rsa.generate", "ecdsa.signingkey"])
    
    #  Look for Web3 wallet interactions
    uses_web3_accounts = "web3.eth.account" in source or "eth_account" in source
    
    assert (has_wallet_class or has_key_generation or uses_web3_accounts) is True, \
        "ystem does not implement digital wallet creation or key managemn"

def test_transaction_processing():
    #equirement to processing payments and secure cryptographic transfers over the blockchain""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    raw_source = get_source_code().lower()
    clean_source = raw_source.replace(" ", "").replace("\n", "")
    
    # verify tTransaction logic exists
    has_tx_logic = any(keyword in clean_source for keyword in [
        "classtransaction", "deftransfer", "defsend", "defcreate_transaction", "send_transaction", "sendrawtransaction"
    ])
    assert has_tx_logic is True, "no transaction processing or transfer logic found"

    # v erify cryptographic security
    has_crypto = any(crypto in clean_source for crypto in [
        "hashlib", "sha256", "ecdsa", "sign(", "verify(", "web3", "cryptography", "rsa", "hash("
    ])
    
    # werify blockchain structures
    has_blockchain = any(chain in clean_source for chain in [
        "classblock", "chain.append", "blockchain", "ledger", "mine(", "web3.eth"
    ])

    assert (has_crypto and has_blockchain) is True, \
        "transactions lack cryptographic security or blockchain structure"