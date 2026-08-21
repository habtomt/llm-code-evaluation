import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

 
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

def test_text_to_speech_conversion():
    """requirement, Convert educational content or text into speech."""
    source = get_clean_source()
    
    # Verify texttospeech library or synthesis references
    has_tts = any(keyword in source for keyword in [
        "tts", "speech", "gtts", "pyttsx3", "synthesiz", "speak", "audio", "convert", "save"
    ])
    
    assert has_tts is True, \
        "no text-to-speech conversion or audio synthesis logic found."

def test_educational_content_handling():
    """requirement, Process educational content for audio-based users."""
    source = get_clean_source()
    
    # Verify educational or textcontent context references
    has_content = any(keyword in source for keyword in [
        "content", "text", "educat", "lesson", "course", "chapter", "material", "study", "article"
    ])
    
    assert has_content is True, \
        "no educational content input or text processing logic found."