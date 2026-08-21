import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["GIT_AUTHOR_NAME"] = "Test Bot"
os.environ["GIT_AUTHOR_EMAIL"] = "bot@test.com"
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

def test_version_control_and_repository():
    """requirement, Use a version control system to push static website files to a repository."""
    source = get_clean_source()
    
    #version control or repository references
    has_vcs = any(keyword in source for keyword in [
        "git", "commit", "push", "repository", "repo", "github", "gitlab", "version"
    ])
    
    assert has_vcs is True, \
        "no version control system or repository logic found."

def test_continuous_deployment_and_web_server():
    #"  requirement, Initiate continuous deployment pipeline and configure web server to serve static content""
    source = get_clean_source()
    
    #Verif CI, CD pipeline
    has_cicd = any(keyword in source for keyword in [
        "pipeline", "ci", "cd", "action", "workflow", "deploy", "transfer"
    ])
    
    # check web server or static file serving
    has_web_server = any(keyword in source for keyword in [
        "nginx", "apache", "server", "static", "html", "http", "serve", "port"
    ])
    
    assert has_cicd is True, \
        "no continuous deployment pipeline logic found"
        
    assert has_web_server is True, \
        "   no web server configuration or static content serving logic found"