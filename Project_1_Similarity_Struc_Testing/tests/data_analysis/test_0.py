import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["MPLBACKEND"] = "Agg"

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

def test_historical_sales_analysis_and_patterns():
    """requirement, Analyze historical sales data to identify trends, seasonal patterns, and factors."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify sales data n historical analysis references
    has_sales_context = any(keyword in source for keyword in [
        "sale", "sales", "revenue", "data", "historical", "dataset", "dataframe"
    ])
    
    # Verify trend or seasonal pattern identification
    has_patterns = any(keyword in source for keyword in [
        "trend", "season", "pattern", "factor", "time", "series", "analysis", "correlat"
    ])
    
    assert has_sales_context is True, \
        "no sales data context or dataset processing found."
        
    assert has_patterns is True, \
        "no trend or seasonal pattern analysis logic found."

def test_statistical_techniques_and_visualization():
    """requirement, Use statistical techniques and visualization tools."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # Verify statistical techniques 
    has_statistics = any(keyword in source for keyword in [
        "pandas", "numpy", "stat", "scipy", "regression", "mean", "median", "model", "calculate"
    ])
    
    # Verify visualization tools 
    has_visualization = any(keyword in source for keyword in [
        "matplotlib", "seaborn", "plot", "plt", "chart", "graph", "visualiz", "show"
    ])
    
    assert has_statistics is True, \
        "no statistical analysis techniques or libraries found."
        
    assert has_visualization is True, \
        "no visualization tools or plotting logic found."