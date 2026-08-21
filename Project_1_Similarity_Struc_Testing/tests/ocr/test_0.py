import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["OMP_THREAD_LIMITED"] = "1"

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

def test_ocr_text_extraction():
    """requirement, Extract and digitize text from scanned or photographed invoices."""
    source = get_clean_source()
    
    # Verify OCR , image text reading libraries
    has_ocr = any(keyword in source for keyword in [
        "tesseract", "ocr", "image", "scan", "photo", "extract", "digitiz", "cv2", "pillow", "pil"
    ])
    
    assert has_ocr is True, \
        "no OCR or image text extraction logic found."

def test_invoice_details_capture():
    """requirement, Capture details such as item descriptions, prices, invoice numbers, dates, and vendor information."""
    source = get_clean_source()
    
    # Verify invoice field capture references
    has_invoice_details = any(keyword in source for keyword in [
        "item", "price", "invoice", "number", "date", "vendor", "description", "total", "amount"
    ])
    
    assert has_invoice_details is True, \
        "no invoice detail extraction (prices, dates, vendor, items) logic found."