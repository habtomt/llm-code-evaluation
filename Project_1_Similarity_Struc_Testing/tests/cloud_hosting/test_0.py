import os
import sys
from pathlib import Path
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["KUBECONFIG"] = "/dev/null"
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["DOCKER_HOST"] = "tcp://127.0.0.1:2375"


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

def test_containerization():
    """requirement,Use containerization to package the web application."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    #verify containerization logic 
    has_containerization = any(keyword in source for keyword in [
        "docker", "container", "image", "dockerfile", "build", "tag", "push", "registry"
    ])
    
    assert has_containerization is True, \
        "no containerization logic (e.g., Docker, images) found."

def test_orchestration_and_scaling():
    """requirement,utilize an orchestration tool to manage deployment, scaling, n running."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify Orchestration Tool 
    has_orchestration = any(keyword in source for keyword in [
        "kubernetes", "k8s", "ecs", "swarm", "orchestrat", "pod", "cluster", "deployment", "service"
    ])
    
    # Verify Scaling Logic 
    has_scaling = any(keyword in source for keyword in [
        "scale", "replica", "hpa", "capacity", "count", "target_capacity"
    ])
    
    assert has_orchestration is True, \
        "no orchestration tool logic (e.g., Kubernetes, ECS, Pods) found."
        
    assert has_scaling is True, \
        "no scaling logic (e.g., replicas, autoscaling) found."