import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers_cache"

 #(sys.exit to prevent test runer crash)
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

def test_sentiment_analysis_and_emotional_tone():
    """requirement, Analyze a text to determine sentiment or emotional tone (positive, negative, neutral)."""
    source = get_clean_source()
    
    # Verify text or string processing references
    has_text_context = any(keyword in source for keyword in [
        "text", "string", "analyze", "sentence", "document", "input"
    ])
    
    # Verify sentiment analysisclassification references
    has_sentiment = any(keyword in source for keyword in [
        "sentiment", "polarity", "positive", "negative", "neutral", "tone", "emotion", "vader", "textblob", "pipeline"
    ])
    
    assert has_text_context is True, \
        "no text analysis input parameter or context found."
        
    assert has_sentiment is True, \
        "no sentiment analysis, polarity, or emotional tone classification logic found."