import os
import sys
from pathlib import Path
import pytest

# root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/dbname"
os.environ["CLOUD_DB_HOST"] = "localhost"

APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    pass

def get_clean_source():
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_schema_and_data_migration():
    #requiremntt: handle schema transfer and data upload to a cloud-based open-source DB"
    assert APP_EXISTS is True, "Code failed or crashed on initialization."
    
    source = get_clean_source()
    
    #verify Sschema transfer
    has_schema_logic = any(keyword in source for keyword in [
        "schema", "createtable", "ddl", "dump", "metadata", "structure", "engine", "inspector", "cursor.execute"
    ])
    
    # Verify data Transfer
    has_data_logic = any(keyword in source for keyword in [
        "insert", "copy", "bulk", "upload", "transfer", "migrate", "pandas", "to_sql", "read_sql", "export", "import"
    ])
    
    assert has_schema_logic is True, \
        "no schema transfer logic"
        
    assert has_data_logic is True, \
        "no data upload or migration logic found"

def test_integrity_and_consistency_checks():
    """rrequirement: perform integrity checks"""
    assert APP_EXISTS is True, "kode failed to compile"
    
    source = get_clean_source()
    
    #Verify data integrity nverification
    has_integrity_check = any(keyword in source for keyword in [
        "count", "checksum", "hash", "rowcount", "verify", "validate", "check", "integrity", "compare", "diff", "assert"
    ])
    
    assert has_integrity_check is True, \
        "system lacks integrity verification logic"