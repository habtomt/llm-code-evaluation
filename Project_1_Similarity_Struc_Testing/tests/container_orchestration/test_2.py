import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

##root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["KUBECONFIG"] = "/dev/null"

# mock kubernetes config loader
with patch("kubernetes.config.load_kube_config", return_value=None), \
     patch("kubernetes.config.load_incluster_config", return_value=None):
    
    
    APP_EXISTS = False
    try:
        import target_app
        APP_EXISTS = True
    except Exception as e:
        print(f"Import failed: {e}")

def get_clean_source():
    #clean source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_dynamic_resource_allocation():
    """requirement, Allocate and manage container resources dynamically."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_resources = any(keyword in source for keyword in [
        "resource", "cpu", "memory", "limit", "request", "allocation", "quota", "resources"
    ])
    
    assert has_resources is True, \
        "no container resource allocation (CPU/Memory requests or limits) found."

def test_real_time_demand_scaling():
    """requirement, Manage resources based on real-time application demand for performance and efficiency."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_demand_scaling = any(keyword in source for keyword in [
        "hpa", "vpa", "autoscal", "scale", "metric", "target", "demand", "utilization"
    ])
    
    assert has_demand_scaling is True, \
        "no dynamic demand-based scaling or performance management logic found."