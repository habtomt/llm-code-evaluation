import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"
os.environ["KUBECONFIG"] = "/mock/kube/config"

 #(sys.exit to prevent test runer crash)
APP_EXISTS = False
try:
    with patch("sys.exit", side_effect=SystemExit):
        import target_app
        APP_EXISTS = True
except SystemExit:
    APP_EXISTS = True
except Exception:
    APP_EXISTS = True

def get_clean_source():
    #clean source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_containerization_and_orchestration():
    """requirement, Package model in a container and deploy to cloud orchestration service."""
    source = get_clean_source()
    
    # Verify containerization, docker references
    has_containerization = any(keyword in source for keyword in [
        "docker", "container", "dockerfile", "image", "build"
    ])
    
    # Verify orchestration or cloud service deployment references
    has_orchestration = any(keyword in source for keyword in [
        "kubernetes", "k8s", "eks", "ecs", "orchestrat", "deployment", "helm", "cluster", "cloud"
    ])
    
    assert has_containerization is True, \
        "no containerization or Docker configuration logic found."
        
    assert has_orchestration is True, \
        "no container orchestration or cloud deployment logic found."

def test_monitoring_and_scaling_rules():
    """requirement, Set up monitoring and scaling rules to adjust to varying loads."""
    source = get_clean_source()
    
    # check monitoring references
    has_monitoring = any(keyword in source for keyword in [
        "monitor", "prometheus", "grafana", "metric", "log", "health", "telemetry"
    ])
    
    # check scaling rules references
    has_scaling = any(keyword in source for keyword in [
        "scale", "autoscal", "hpa", "replica", "load", "capacity", "threshold"
    ])
    
    assert has_monitoring is True, \
        "no system or application monitoring logic found."
        
    assert has_scaling is True, \
        "no scaling rules or auto-scaling configuration found."