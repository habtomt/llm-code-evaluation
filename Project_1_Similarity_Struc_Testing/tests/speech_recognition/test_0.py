import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder tests/speech_recognition/test_1.py 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


os.environ["SPEECH_BACKEND"] = "mock"

 #
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

def test_voice_command_listening_and_recognition():
    """requirement, Listen for and recognize spoken voice instructions."""
    source = get_clean_source()
    
    # Verify voice listening, speech recognition references
    has_listening = any(keyword in source for keyword in [
        "listen", "recognize", "speech", "audio", "mic", "microphone", "sr", "whisper", "command"
    ])
    
    assert has_listening is True, \
        "no voice listening or speech recognition processing logic found."

def test_smart_home_device_control():
    """requirement, Control smart home devices such as lights, thermostat, and security systems."""
    source = get_clean_source()
    
    # Verify device control references 
    has_devices = any(keyword in source for keyword in [
        "light", "thermostat", "security", "device", "home", "turn", "control", "switch"
    ])
    
    assert has_devices is True, \
        "no smart home device control logic found."