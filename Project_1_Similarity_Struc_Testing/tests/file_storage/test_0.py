import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder    (tests/cloud_storage/test_0.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags(Prevent unwanted cloud credential errors on import)
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "DefaultEndpointsProtocol=https;AccountName=mock;AccountKey=mock;EndpointSuffix=core.windows.net"

# (sys.exit to prevent test runer crash)
APP_EXISTS = False
try:
    with patch("sys.exit", side_effect=SystemExit):
        import target_app
        APP_EXISTS = True
except SystemExit:
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

def test_cloud_storage_file_operations():
    """requirement, Integrate cloud storage service enabling uploads, downloads, and metadata management."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify file upload and download references
    has_transfer = any(keyword in source for keyword in [
        "upload", "download", "put", "get", "transfer", "file"
    ])
    
    # Verify metadata management references
    has_metadata = any(keyword in source for keyword in [
        "metadata", "property", "attribute", "tag", "header", "info"
    ])
    
    assert has_transfer is True, \
        "no file upload or download logic found."
        
    assert has_metadata is True, \
        "no file metadata management logic found."

def test_api_compatibility_and_synchronization():
    """requirement, Ensure compatibility with APIs for data transfer and multi-platform synchronization."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify API integration or cloud SDK 
    has_api = any(keyword in source for keyword in [
        "boto3", "azure", "google", "s3", "blob", "api", "client", "request", "sdk"
    ])
    
    # Verify synchronization 
    has_sync = any(keyword in source for keyword in [
        "sync", "synchroniz", "replicate", "mirror", "cross", "platform"
    ])
    
    assert has_api is True, \
        "no cloud API or SDK data transfer logic found."
        
    assert has_sync is True, \
        "no synchronization or multi-platform handling found."