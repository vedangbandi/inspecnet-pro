import importlib.util
import os
import torch
from pathlib import Path

class SystemValidator:
    REQUIRED_MODULES = [
        "PySide6",
        "torch",
        "torchvision",
        "pandas",
        "numpy",
        "matplotlib",
        "sklearn",
        "PIL",
        "onnx",
        "onnxruntime",
        "psutil"
    ]
    
    MARKER_FILE = ".sys_ready"

    @staticmethod
    def check_modules():
        """Returns a list of missing modules."""
        missing = []
        for module in SystemValidator.REQUIRED_MODULES:
            if importlib.util.find_spec(module) is None:
                missing.append(module)
        return missing

    @staticmethod
    def check_cuda():
        """Returns (is_available, device_name)"""
        available = torch.cuda.is_available()
        name = torch.cuda.get_device_name(0) if available else "CPU"
        return available, name

    @staticmethod
    def is_first_run():
        """Checks if the system has been validated before."""
        return not os.path.exists(SystemValidator.MARKER_FILE)

    @staticmethod
    def mark_as_ready():
        """Creates a marker file to skip full checks next time."""
        Path(SystemValidator.MARKER_FILE).touch()
