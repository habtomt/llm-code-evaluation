import os
import sys
from pathlib import Path
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["CLOUD_API_TOKEN"] = "mock_token"


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

def test_load_monitoring():
    """requirement, Adjusts resources based on current load (requires monitoring load metrics)"""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # look for load monitoring logic
    has_monitoring = any(keyword in source for keyword in [
        "cpu", "memory", "load", "metric", "cloudwatch", "monitor", "utilization", "threshold", "alarm"
    ])
    
    assert has_monitoring is True, \
        "no logic found for monitoring database load or metrics."

def test_auto_scaling_actions():
    """requirement, Adding or removing instances and optimizing resource allocation."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # look for Scaling actions
    has_scaling = any(keyword in source for keyword in [
        "scale", "capacity", "instance", "add", "remove", "modify", "allocate", "boto3", "resize", "update"
    ])
    
    assert has_scaling is True, \
        "no logic found for scaling actions (adding/removing instances or modifying capacity)."