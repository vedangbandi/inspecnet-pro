import torch
import sys
import os

def check():
    print("Python Executable:", sys.executable)
    print("PyTorch Version:", torch.__version__)
    print("CUDA Available:", torch.cuda.is_available())
    print("CUDA Version:", torch.version.cuda)
    print("CuDNN Backend:", torch.backends.cudnn.enabled)
    
    if torch.cuda.is_available():
        print("Device Count:", torch.cuda.device_count())
        print("Current Device:", torch.cuda.current_device())
        print("Device Name:", torch.cuda.get_device_name(0))
    else:
        print("!!! NO GPU DETECTED !!!")
        print("Common causes: Incorrect PyTorch version installed (CPU-only), or missing NVIDIA Drivers.")

if __name__ == "__main__":
    check()
