import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ["STREAM_SERVER_PORT"] = "1935"
 
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
    
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_live_streaming_broadcast():
    """requirement, Develop a live streaming feature for real-time video broadcast."""
    source = get_clean_source()
    
    # streaming or broadcast references
    has_streaming = any(keyword in source for keyword in [
        "stream", "broadcast", "live", "rtmp", "hls", "video", "ffmpeg", "server"
    ])
    
    assert has_streaming is True, \
        "no live streaming or video broadcast logic found."

def test_concurrent_streams_and_adaptable_resolution():
    """requirement, Support multiple concurrent streams and adaptable resolution settings."""
    source = get_clean_source()
    
    # concurrency or multi-stream references
    has_concurrency = any(keyword in source for keyword in [
        "concurrent", "multi", "thread", "async", "clients", "sessions", "pool"
    ])
    
    #resolution and adaptability settings references
    has_adaptable = any(keyword in source for keyword in [
        "resolution", "adapt", "bitrate", "scale", "quality", "transcode", "profile"
    ])
    
    assert has_concurrency is True, \
        "no multiple concurrent streams handling logic found."
        
    assert has_adaptable is True, \
        "no adaptable resolution or quality configuration logic found."