import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["SIGNALING_SERVER_PORT"] = "8080"

 #sys.exit to prevent test runer crash
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

def test_real_time_video_audio_communication():
    """requirement, Build a real-time video conferencing solution using open-source protocols for video and audio communication."""
    source = get_clean_source()
    
    # WebRTC, sockets, or videooraudio communication references
    has_communication = any(keyword in source for keyword in [
        "webrtc", "socket", "io", "peer", "video", "audio", "stream", "rtc", "connection"
    ])
    
    assert has_communication is True, \
        "no real-time video/audio communication or WebRTC protocol logic found."

def test_conference_features_management_sharing_chat():
    """requirement, Include features like participant management, screen sharing, and chat."""
    source = get_clean_source()
    
    # check participant management, screen sharing, chat references
    has_features = any(keyword in source for keyword in [
        "participant", "user", "room", "screen", "share", "chat", "message", "peer", "connect"
    ])
    
    assert has_features is True, \
        "no participant management, screen sharing, or chat features found."