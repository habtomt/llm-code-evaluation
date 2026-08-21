import os
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ["KUBECONFIG"] = "/dev/null"
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"

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

def test_multi_cloud_container_deployment():
    """requirement, Deploy containerized applications across multiple cloud environments."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify containerization and multi-cloud deployment
    has_containers = any(keyword in source for keyword in [
        "container", "docker", "image", "pod", "service", "deployment"
    ])
    
    has_multi_cloud = any(keyword in source for keyword in [
        "multi", "cloud", "aws", "gcp", "azure", "cluster", "hybrid", "environment"
    ])
    
    assert has_containers is True, \
        "no containerization references found."
        
    assert has_multi_cloud is True, \
        "no multi-cloud or cross-environment deployment logic found."

def test_abstracted_management_platform():
    """requirement, Utilize a management platform that abstracts cloud-specific configurations."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    #Verify orchestration
    has_abstraction_platform = any(keyword in source for keyword in [
        "kubernetes", "k8s", "terraform", "nomad", "rancher", "crossplane", "helm", "orchestrat", "manager"
    ])
    
    assert has_abstraction_platform is True, \
        "no abstraction management platform (e.g., Kubernetes, Terraform, Helm) found."