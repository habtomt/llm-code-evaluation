import os
import sys
from pathlib import Path
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/dev/null"


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

def test_database_on_virtual_machine():
    """requirement, Deploy a database system on a virtual machine."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # verify database system 
    has_database = any(keyword in source for keyword in [
        "postgres", "mysql", "mongodb", "database", "db", "sql", "redis", "engine"
    ])
    
    # verify vm or compute instance provisioning
    has_vm = any(keyword in source for keyword in [
        "ec2", "compute", "vm", "instance", "virtual", "machine", "droplet", "host"
    ])
    
    assert has_database is True, \
        "no database system integration found."
        
    assert has_vm is True, \
        "no virtual machine or compute provisioning reference found."

def test_automated_scaling_and_monitoring():
    """requirement, Configure automated scaling and integrate monitoring for performance and alerts."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # verify scaling configuration 
    has_scaling = any(keyword in source for keyword in [
        "scale", "scaling", "autoscal", "replica", "capacity", "expand", "auto"
    ])
    
    # verify monitoring/metrics and alerts
    has_monitoring = any(keyword in source for keyword in [
        "monitor", "metric", "alert", "alarm", "cloudwatch", "prometheus", "grafana", "performance"
    ])
    
    assert has_scaling is True, \
        "no automated scaling configuration found."
        
    assert has_monitoring is True, \
        "no performance monitoring or alerting logic found."