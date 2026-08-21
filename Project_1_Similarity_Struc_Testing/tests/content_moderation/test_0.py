import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

##root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["OPENAI_API_KEY"] = "mock_openai_key"
os.environ["HUGGINGFACE_API_KEY"] = "mock_hf_key"

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

def test_automated_detection_and_removal():
    """requirement, Implement automated methods to detect and remove inappropriate posts or comments."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_detection = any(keyword in source for keyword in [
        "detect", "moderate", "filter", "remove", "delete", "flag", "inappropriate", "violation"
    ])
    
    has_forum_context = any(keyword in source for keyword in [
        "post", "comment", "forum", "message", "text", "content"
    ])
    
    assert has_detection is True, \
        "no automated detection or removal moderation logic found."
        
    assert has_forum_context is True, \
        "no post, comment, or forum context found."

def test_nlp_offensive_language_and_spam_scanning():
    """requirement, Use natural language processing to scan for offensive language, spam, or guidelines violations."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_nlp = any(keyword in source for keyword in [
        "nlp", "natural", "language", "transformer", "bert", "openai", "classifier", "model", "tokenize", "regex", "word", "spam", "offensive"
    ])
    
    assert has_nlp is True, \
        "no natural language processing (NLP), classification, or keyword scanning logic found."