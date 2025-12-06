import importlib
import sys

required = [
    "PySide6",
    "torch",
    "torchvision",
    "PIL",
    "matplotlib",
    "numpy",
    "PyInstaller"
]

missing = []
print(f"Checking Python: {sys.version}")

for lib in required:
    try:
        importlib.import_module(lib)
        print(f" [x] {lib}")
    except ImportError:
        # Special case for Pillow which is imported as PIL
        if lib == "PIL":
            try:
                importlib.import_module("PIL")
                print(f" [x] {lib}")
            except:
                print(f" [ ] {lib} (MISSING)")
                missing.append("Pillow")
        else:
            print(f" [ ] {lib} (MISSING)")
            missing.append(lib)

if missing:
    print(f"\nMISSING MODULES: {', '.join(missing)}")
    sys.exit(1)
else:
    print("\nALL MODULES FOUND.")
    sys.exit(0)
