import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["GEOLOCATION_API_KEY"] = "mock_geo_key"
os.environ["MAPS_API_KEY"] = "mock_maps_key"

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

def test_geographic_location_detection():
    """requirement, Detect user's geographic location in real-time."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify location detection references
    has_location = any(keyword in source for keyword in [
        "location", "geolocat", "gps", "coordinate", "latitude", "longitude", "position", "realtime", "real-time"
    ])
    
    assert has_location is True, \
        "no user geographic location detection logic found."

def test_proximity_targeted_advertisements():
    """requirement, Deliver targeted advertisements based on proximity to nearby businesses."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify business proximity and advertising references
    has_business_proximity = any(keyword in source for keyword in [
        "business", "store", "nearby", "proximity", "distance", "radius", "local"
    ])
    
    has_ads = any(keyword in source for keyword in [
        "advertis", "ad", "target", "promotion", "offer", "campaign", "deal"
    ])
    
    assert has_business_proximity is True, \
        "no nearby business proximity calculation logic found."
        
    assert has_ads is True, \
        "no targeted advertisement delivery logic found."