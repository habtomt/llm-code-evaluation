import os
import sys
from pathlib import Path
import pytest

##root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["KUBECONFIG"] = "/dev/null"


APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    pass

def get_clean_source():
    #clean source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_redundant_and_distributed_instances():
    #"""requirement, Configure redundant and distributed container instances"""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify redundancy, replicas or distribution across nodes
    has_redundancy = any(keyword in source for keyword in [
        "replica", "redundant", "replicaset", "deployment", "distributed", "node", "zone", "cluster"
    ])
    
    #erify container
    has_containers = any(keyword in source for keyword in [
        "container", "pod", "service", "instance", "docker"
    ])
    
    assert has_redundancy is True, \
        "no redundancy or replica scaling configuration found."
        
    assert has_containers is True, \
        "no container or pod instance definitions found."

def test_uptime_and_automatic_failover():
    """requirement, Ensure application uptime and handle failover automatically."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    #   Verify failover, health checks, restart policies,or high availability
    has_failover = any(keyword in source for keyword in [
        "failover", "health", "probe", "restart", "availability", "liveness", "readiness", "strategy", "fault"
    ])
    
    assert has_failover is True, \
        "no automatic failover, health check, or high availability logic found."