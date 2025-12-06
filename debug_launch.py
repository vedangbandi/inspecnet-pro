
import sys
import traceback

print("Attempting to import main...")
try:
    import main
    print("Import successful. Running app...")
    main.app = main.DefectDetectionApp()
    main.app.mainloop()
except Exception:
    print("CRASH DETECTED:")
    traceback.print_exc()
except SystemExit as e:
    print(f"System Exit: {e}")
