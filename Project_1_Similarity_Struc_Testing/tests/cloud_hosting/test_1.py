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

def test_scheduled_backup_tool():
    """requirement, Set up a scheduled task using an open-source tool for regular backups."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify open-source backup tool 
    has_backup_tool = any(keyword in source for keyword in [
        "rclone", "tar", "restic", "duplicity", "backup", "snapshot", "zip", "gzip"
    ])
    
    # Verify scheduling mechanism 
    has_scheduling = any(keyword in source for keyword in [
        "schedule", "cron", "every", "time", "sleep", "interval", "loop", "timer"
    ])
    
    assert has_backup_tool is True, \
        "no open-source backup tool logic (e.g., rclone, tar, restic) found."
        
    assert has_scheduling is True, \
        "no scheduling mechanism (e.g., schedule, cron, interval) found."

def test_cloud_storage_and_monitoring():
    """requirement, Store backups in a cloud storage bucket and implement a monitoring script."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify cloud storage destination 
    has_cloud_storage = any(keyword in source for keyword in [
        "s3", "bucket", "gcs", "blob", "cloud", "storage", "upload", "remote"
    ])
    
    # Verify monitoring logic
    has_monitoring = any(keyword in source for keyword in [
        "monitor", "log", "check", "success", "verify", "error", "status", "try"
    ])
    
    assert has_cloud_storage is True, \
        "no cloud storage bucket integration (e.g., S3, GCS, bucket) found."
        
    assert has_monitoring is True, \
        "no monitoring or validation logic found."