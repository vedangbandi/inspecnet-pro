# InspecNet Pro - Training Application

## Overview
Complete end-to-end deep learning training application with professional UI and advanced features.

## Key Features

### 1. **Dataset Management**
- Visual dataset browser with thumbnail previews
- Auto-detection of image classes
- Support for train/val/test splits
- Real-time dataset statistics

### 2. **Training Configuration**
- **Model Selection**: MobileNetV2, ResNet50, EfficientNetB0
- **Hyperparameters**:
  - Epochs (default: 20, recommended: 20-50)
  - Batch Size (default: 32)
  - Learning Rate (default: 0.001)
- **Early Stopping**:
  - Toggle ON/OFF
  - Patience: 10 epochs (monitors validation accuracy)
  - Prevents overfitting and saves training time
- **Abort Training**: Cancel training mid-process

### 3. **Real-Time Monitoring**
- Live training logs with color-coded messages
- Validation accuracy plot (train vs val)
- Global progress bar across all epochs
- KPI Cards:
  - Best Validation Accuracy
  - Total Training Time
- Batch-level loss updates

### 4. **Model Export**
- **ONNX Export**: One-click export to ONNX format
- Use cases:
  - Deploy in C++/C#/Java applications
  - Run in web browsers (ONNX Runtime Web)
  - Mobile deployment (iOS/Android)
  - 2-10x faster inference

### 5. **Inference**
- Load external images for prediction
- Real-time classification with confidence scores
- Visual feedback

## Training Best Practices

### Early Stopping Configuration
- **When to use**: Always recommended to prevent overfitting
- **Patience setting**:
  - Small datasets: 5-7 epochs
  - Medium datasets: 10-15 epochs (default)
  - Large datasets: 15-20 epochs
- **How it works**: Stops training when validation accuracy doesn't improve for N consecutive epochs

### Recommended Settings for High Accuracy
1. **Epochs**: Start with 20-30, increase if early stopping triggers too soon
2. **Batch Size**: 
   - Small GPU memory: 16-32
   - Large GPU memory: 64-128
3. **Learning Rate**: 
   - Start: 0.001 (default)
   - If accuracy plateaus early: try 0.0001
   - If training unstable: try 0.0005
4. **Early Stopping**: 
   - Enable: Yes
   - Patience: 10-15 epochs

### Achieving 85%+ Accuracy
- Ensure dataset quality (balanced classes, clean labels)
- Use data augmentation (already enabled: ColorJitter, RandomHorizontalFlip)
- Train for sufficient epochs (20-50)
- Monitor validation accuracy plot for convergence
- Use early stopping with patience ≥ 10

## UI Enhancements
- **Modern Design**: Glassmorphism, gradients, smooth animations
- **Color Scheme**: Dark mode with cyan/green accents
- **Tooltips**: Hover over controls for guidance
- **Status Indicators**: Color-coded pills (IDLE/TRAINING/COMPLETE/ERROR)
- **Responsive Layout**: Optimized for 1400x900 resolution

## Technical Stack
- **Framework**: PySide6 (Qt)
- **Deep Learning**: PyTorch 2.6.0 + CUDA
- **Visualization**: Matplotlib
- **Export**: ONNX Runtime

## File Structure
```
triple-sagan/
├── main.py                 # Main application
├── src/
│   ├── dataset.py         # Dataset handling
│   ├── model.py           # Model factory
│   ├── trainer.py         # Training logic
│   ├── exporter.py        # ONNX export
│   ├── ui_styles.py       # UI styling
│   └── ui_components.py   # Custom widgets
├── checkpoints/           # Saved models
└── dist/                  # Executable build
```

## Running the Application

### From Python
```powershell
python main.py
```

### From Executable
```powershell
cd dist\InspecNetPro
.\InspecNetPro.exe
```

## Building Executable
```powershell
pyinstaller --name InspecNetPro --onedir --console --clean \
  --hidden-import=sklearn.metrics \
  --hidden-import=PIL \
  --hidden-import=torchvision \
  --hidden-import=torch \
  --hidden-import=onnx \
  --hidden-import=onnxruntime \
  main.py
```

## Troubleshooting

### Low Accuracy (<85%)
1. Increase epochs to 30-50
2. Increase early stopping patience to 15-20
3. Try different model architectures (ResNet50 for better accuracy)
4. Check dataset quality and balance
5. Reduce learning rate to 0.0005

### Training Too Slow
1. Reduce batch size if GPU memory is full
2. Use MobileNetV2 for faster training
3. Enable early stopping to avoid unnecessary epochs

### Early Stopping Triggers Too Soon
1. Increase patience (15-20 epochs)
2. Check if validation accuracy is actually improving
3. Try reducing learning rate for smoother convergence

## Version History
- **v1.0**: Initial release with basic training
- **v2.0**: Added early stopping and abort functionality
- **v2.1**: Fixed early stopping to monitor accuracy (not loss)
- **v2.2**: UI enhancements, KPI cards, tooltips, better defaults

## License
Enterprise Edition - Internal Use Only
