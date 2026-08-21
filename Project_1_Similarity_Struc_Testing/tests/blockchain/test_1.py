import os
import sys
from pathlib import Path
import pytest

# root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# ntw gags
os.environ["WEB3_PROVIDER_URI"] = "http://127.0.0.1:8545" 
os.environ["INFURA_URL"] = "http://127.0.0.1:8545"

APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    
    pass

def get_clean_source():
    
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_supply_chain_tracking():
    """requirement. iImplement smart contracts tracking products and streamlining processes"""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # verify smart Contract orSupply chain exists
    has_architecture = any(keyword in source for keyword in [
        "classsupplychain", "contractsupplychain", "classsmartcontract", "smartcontract"
    ])
    
    #verify product entity exists
    has_entity = any(keyword in source for keyword in [
        "product", "item", "batch", "asset", "shipment"
    ])
    
    #   verify state changes
    has_tracking = any(keyword in source for keyword in [
        "status", "state", "location", "history", "stage", "manufactur", "ship", "deliver"
    ])
    
    assert (has_architecture or has_entity) is True, \
        "no Supply chain architecture or product entities found"
        
    assert has_tracking is True, \
        "no logic found for tracking product states."

def test_authenticity_and_conditions():
    #requirement, verifying authenticity and predetermined conditions coded within the contracts
    assert APP_EXISTS is True, "kode failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # verify authenticity   Checks
    has_authenticity = any(keyword in source for keyword in [
        "verify", "authentic", "hash", "signature", "proof", "owner", "msg.sender"
    ])
    
    #verify predetermined Conditions 
    has_conditions = any(keyword in source for keyword in [
        "require(", "assert", "modifier", "onlyowner", "is_authentic", "condition", "ifmsg.sender", "raise", "exception"
    ])
    
    assert (has_authenticity and has_conditions) is True, \
        "system lacks authenticity verification or conditional enforcement logic"