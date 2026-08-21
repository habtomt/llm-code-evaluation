import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# env gags
os.environ["MPLBACKEND"] = "Agg"

# create dummy csv content
csv_content = (
    "customer_id,age,annual_income,spending_score\n"
    "1,25,15000,39\n"
    "2,42,85000,81\n"
    "3,29,18000,6\n"
    "4,33,42000,77\n"
    "5,45,120000,90\n"
)

# Seed the CSV file in the root directory 
root_csv_path = ROOT_DIR / "customer_data.csv"
try:
    with open(root_csv_path, "w", encoding="utf-8") as f:
        f.write(csv_content)
except Exception:
    pass


TEST_DIR = tempfile.mkdtemp()
os.chdir(TEST_DIR)
with open("customer_data.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

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
        with open(root_csv_path.parent / "target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_customer_clustering_algorithms():
    """requirement, Use clustering algorithms to group customers based on behavior and metrics."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_clustering = any(keyword in source for keyword in [
        "cluster", "kmeans", "dbscan", "sklearn", "fit_predict", "unsupervised", "group"
    ])
    
    has_customer_context = any(keyword in source for keyword in [
        "customer", "purchas", "behavior", "demographic", "metric", "data", "feature"
    ])
    
    assert has_clustering is True, \
        "no clustering algorithm logic (e.g., KMeans, DBSCAN) found."
        
    assert has_customer_context is True, \
        "no customer data or behavioral context found."

def test_tailored_marketing_strategies():
    """requirement, Tailor marketing strategies based on customer segments."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    has_marketing = any(keyword in source for keyword in [
        "market", "strat", "segment", "campaign", "tailor", "persona", "target", "recommend"
    ])
    
    assert has_marketing is True, \
        "no marketing strategy or segmentation tailoring logic found."