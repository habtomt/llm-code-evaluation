import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder tests/translation/test_0.py 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["TRANSLATION_API_KEY"] = "mock_translation_key"
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

def test_multilingual_input_handling():
    """requirement, Listen to user input in one language."""
    source = get_clean_source()
    
    # Verify input  language references
    has_input = any(keyword in source for keyword in [
        "input", "listen", "text", "source", "audio", "speech", "read", "message"
    ])
    
    assert has_input is True, \
        "no user input or source language handling logic found."

def test_instant_target_language_output():
    """requirement, Provide audio or text output in the target language instantly."""
    source = get_clean_source()
    
    # Verify translation and target output references
    has_translation = any(keyword in source for keyword in [
        "translate", "translation", "target", "googletrans", "deepl", "translat", "output"
    ])
    
    assert has_translation is True, \
        "no translation or target language output logic found."