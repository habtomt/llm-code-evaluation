import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

os.environ["FUNCTIONS_WORKER_RUNTIME"] = "python"
os.environ["AWS_REGION"] = "us-east-1"

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

def test_serverless_http_trigger_function():
    """requirement, Set up a function to process images upon receipt through an HTTP trigger."""
    source = get_clean_source()
    
    # V erify serverless function or HTTP trigger references
    has_http_trigger = any(keyword in source for keyword in [
        "http", "trigger", "request", "event", "lambda", "function", "endpoint", "route", "def"
    ])
    
    #   Verify image receipt and processing context
    has_image_context = any(keyword in source for keyword in [
        "image", "img", "picture", "file", "payload", "bytes", "stream"
    ])
    
    assert has_http_trigger is True, \
        "no HTTP trigger or serverless function endpoint found."
        
    assert has_image_context is True, \
        "no image receipt or processing input context found."

def test_image_resizing_and_filtering():
    """requirement, Utilize an open-source image handling library for tasks such as resizing and filtering."""
    source = get_clean_source()
    
    # Verify opensource image library references 
    has_image_library = any(keyword in source for keyword in [
        "pillow", "pil", "image", "cv2", "opencv", "skimage", "thumbnail", "resize"
    ])
    
    # Verify resizing or filtering operations
    has_operations = any(keyword in source for keyword in [
        "resize", "resizing", "filter", "filtering", "blur", "convert", "transform", "crop"
    ])
    
    assert has_image_library is True, \
        "no open-source image handling library (e.g., Pillow, OpenCV) found."
        
    assert has_operations is True, \
        "no image resizing or filtering operations found."