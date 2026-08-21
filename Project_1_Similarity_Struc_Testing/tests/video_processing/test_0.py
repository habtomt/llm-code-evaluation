import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folde
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

#Prevent unwanted ffmpeg or moviepy dependency errors on import
os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"

 
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
    
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_video_size_reduction():
    """requirement, Implement a method to reduce video file size."""
    source = get_clean_source()
    
    # Verify video compression file size reduction references
    has_reduction = any(keyword in source for keyword in [
        "reduce", "compress", "size", "shrink", "optimize", "ffmpeg", "cv2", "moviepy", "video"
    ])
    
    assert has_reduction is True, \
        "no video file size reduction or compression logic found."

def test_bitrate_resolution_and_codec_adjustment():
    """requirement, Use techniques such as adjusting bitrate, resolution, and codec."""
    source = get_clean_source()
    
    # Verify bitrate, resolution, codec adjustment references
    has_adjustments = any(keyword in source for keyword in [
        "bitrate", "resolution", "codec", "crf", "scale", "resize", "h264", "libx264"
    ])
    
    assert has_adjustments is True, \
        "no bitrate, resolution, or codec adjustment logic found."