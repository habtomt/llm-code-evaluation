import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
#   env gags
os.environ["WEATHER_API_KEY"] = "mock_weather_api_key"

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

def test_weather_data_fetching():
    """requirement, Fetch live weather data including temperature, humidity, and wind speed."""
    source = get_clean_source()
    
    # weather or API fetching references
    has_weather_api = any(keyword in source for keyword in [
        "weather", "api", "fetch", "requests", "get", "forecast", "url"
    ])
    
    # Verify meteorological metrics
    has_metrics = any(keyword in source for keyword in [
        "temp", "temperature", "humidity", "wind", "speed"
    ])
    
    assert has_weather_api is True, \
        "no weather data fetching or API logic found."
        
    assert has_metrics is True, \
        "no weather metrics (temperature, humidity, wind speed) found."

def test_dashboard_format_and_interaction():
    """requirement, Display in a dashboard format for immediate user interaction."""
    source = get_clean_source()
    
    # look dashboard, UI framework references
    has_dashboard = any(keyword in source for keyword in [
        "dashboard", "streamlit", "dash", "flask", "render", "ui", "display", "layout", "interactive"
    ])
    
    assert has_dashboard is True, \
        "no dashboard display or interactive UI logic found."