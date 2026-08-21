import os
import sys
from pathlib import Path
import pytest

# root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


os.environ["WEB3_PROVIDER_URI"] = "http://127.0.0.1:8545" 
os.environ["INFURA_URL"] = "http://127.0.0.1:8545"


APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    
    pass

def get_clean_source():
    #read n clean the source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            #           strip spaces, newlines, and quotes 
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_defi_services():
    #requirement, platform allowing users to access financial services such as lending, borrowing, and trading.""
    
    source = get_clean_source()
    
    # look for Lending logic
    has_credit_logic = any(keyword in source for keyword in [
        "lend", "borrow", "loan", "collateral", "interest", "deposit", "withdraw", "liquidity"
    ])
    
    # llook for trading logic
    has_trading_logic = any(keyword in source for keyword in [
        "trade", "swap", "exchange", "orderbook", "market", "bid", "ask", "pair"
    ])
    
    
    assert (has_credit_logic or has_trading_logic) is True, \
        "no DeFi logic found /missing lending, borrowing or trading implementations"

def test_blockchain_architecture():
    #requiremnt: uUtilize blockchain to offer transparency and security without intermediaries
    
    source = get_clean_source()
    
    # verify Blockchain Architecture Smart contracts, ledgers, web3
    has_blockchain = any(keyword in source for keyword in [
        "contract", "web3", "solidity", "decentralized", "ledger", "blockchain", "block", "pool"
    ])
    
    # vverify Security Mechanisms 
    has_security = any(keyword in source for keyword in [
        "hash", "verify", "signature", "secure", "crypto", "balanceof", "msg.sender", "require("
    ])
    
    assert (has_blockchain and has_security) is True, \
        "system lacks blockchain architecture or cryptographic security mechanisms"