import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder (tests/ecommerce/test_0.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags(Prevent unwanted web server execution during import)
os.environ["FLASK_ENV"] = "testing"
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

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

def test_ui_ux_dynamic_content_and_pricing():
    """requirement, Add dynamic content loading, real-time price updates, and rich product descriptions."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify dynamic content loading or pricing references
    has_dynamic_content = any(keyword in source for keyword in [
        "dynamic", "load", "content", "render", "template", "dom", "append"
    ])
    
    has_pricing_or_descriptions = any(keyword in source for keyword in [
        "price", "update", "realtime", "real-time", "description", "product", "item"
    ])
    
    assert has_dynamic_content is True, \
        "no dynamic content loading or UI rendering logic found."
        
    assert has_pricing_or_descriptions is True, \
        "no real-time price updates or product description logic found."

def test_ajax_calls_without_page_reload():
    """requirement, Implement AJAX calls to fetch additional product details without reloading the page."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify AJAX n asynchronous fetching references 
    has_ajax = any(keyword in source for keyword in [
        "ajax", "fetch", "axios", "async", "xmlhttprequest", "route", "endpoint", "api", "json"
    ])
    
    assert has_ajax is True, \
        "no AJAX, fetch, or asynchronous endpoint logic found for asynchronous loading."