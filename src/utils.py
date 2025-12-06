import logging
import os
import sys

def setup_logger(name=__name__, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        
    return logger

logger = setup_logger("DefectDetection")

def validate_image_file(filepath):
    """Check if file is a valid image."""
    from PIL import Image
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True
    except Exception:
        return False
