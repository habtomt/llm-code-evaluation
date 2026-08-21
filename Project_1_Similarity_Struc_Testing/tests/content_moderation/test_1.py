import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["OPENAI_API_KEY"] = "mock_openai_key"
os.environ["HUGGINGFACE_API_KEY"] = "mock_hf_key"

 #(sys.exit to prevent test runer crash)
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

def test_harmful_content_filtering_and_ml():
    """requirement, Filter and flag harmful content (hate speech, harassment, misinformation) using ML"""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # verify harmful content categories 
    has_harmful_categories = any(keyword in source for keyword in [
        "hate", "harass", "misinformation", "harmful", "toxic", "abuse", "offensive"
    ])
    
    #Verify machine learning or classification algorithm 
    has_ml = any(keyword in source for keyword in [
        "model", "classifier", "ml", "machine", "learning", "predict", "nlp", "transformer", "score"
    ])
    
    assert has_harmful_categories is True, \
        "no harmful content detection (hate speech, harassment, misinformation) logic found."
        
    assert has_ml is True, \
        "no machine learning or classification algorithm logic found."

def test_content_prioritization_and_severity():
    """requirement, Prioritize content for review based on severity and user reports."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify prioritization or sorting ceverity weight
    has_prioritization = any(keyword in source for keyword in [
        "priorit", "severity", "rank", "sort", "weight", "queue", "urgent", "flag"
    ])
    
    #vVerify user reports handling
    has_user_reports = any(keyword in source for keyword in [
        "report", "user", "complaint", "feedback", "submit"
    ])
    
    assert has_prioritization is True, \
        "no content prioritization or severity-based review logic found."
        
    assert has_user_reports is True, \
        "no user reporting mechanism found."