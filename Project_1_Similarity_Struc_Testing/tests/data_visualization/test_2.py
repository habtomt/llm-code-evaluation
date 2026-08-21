import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["MPLBACKEND"] = "Agg"

 #      (sys.exit to prevent test runer crash)
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

def test_website_traffic_analysis():
    """requirement, Examine website traffic data for visitor behavior, peak times, and demographics."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify website traffic or visitor behavior context
    has_traffic_context = any(keyword in source for keyword in [
        "traffic", "visitor", "session", "pageview", "user", "click", "web", "site"
    ])
    
    # Verify peak times, demographics, or engagement metrics
    has_metrics = any(keyword in source for keyword in [
        "peak", "time", "hour", "demographic", "engagement", "metric", "duration", "bounce", "rate"
    ])
    
    assert has_traffic_context is True, \
        "no website traffic or visitor behavior context found."
        
    assert has_metrics is True, \
        "no peak traffic, demographics, or engagement metrics analysis found."

def test_statistical_techniques_and_visualizations():
    """requirement, Use statistical techniques and create clear visualizations."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    #verify statistical techniques or libraries 
    has_statistics = any(keyword in source for keyword in [
        "pandas", "numpy", "stat", "mean", "median", "groupby", "aggregate", "calculate"
    ])
    
    #Verify visualization tools
    has_visualization = any(keyword in source for keyword in [
        "matplotlib", "seaborn", "plotly", "plot", "plt", "chart", "graph", "visualiz"
    ])
    
    assert has_statistics is True, \
        "no statistical analysis techniques or libraries found."
        
    assert has_visualization is True, \
        "no visualization tools or plotting logic found."