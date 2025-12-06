# InspecNet Pro - Material Defect Detection System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0-red.svg)](https://pytorch.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Professional end-to-end deep learning training application for material defect detection with real-time monitoring, early stopping, and ONNX export.**

![InspecNet Pro Screenshot](docs/screenshot.png)

## 🌟 Key Features

- ✅ **Visual Dataset Browser** - Thumbnail previews and auto-class detection
- ✅ **3 Model Architectures** - MobileNetV2, ResNet50, EfficientNetB0
- ✅ **Smart Early Stopping** - Monitors validation accuracy (achieves 85%+)
- ✅ **Real-Time Monitoring** - Live logs, accuracy plots, and KPI cards
- ✅ **ONNX Export** - One-click model conversion for production deployment
- ✅ **Abort Training** - Cancel training mid-process
- ✅ **Professional UI** - Dark mode with glassmorphism effects
- ✅ **GPU Auto-Detection** - Automatic CUDA utilization

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- NVIDIA GPU with CUDA (optional, but recommended for 5-10x speedup)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/inspecnet-pro.git
cd inspecnet-pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dataset Structure

```
your_dataset/
├── class1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── class2/
│   └── ...
└── class3/
    └── ...
```

## 📊 Usage

### 1. Load Dataset
- Click **"Dataset"** tab
- Browse to your dataset folder
- Click **"Load Dataset"**

### 2. Configure Training
- Click **"Training"** tab
- **Recommended settings for 85%+ accuracy**:
  - Model: ResNet50
  - Epochs: 30-50
  - Batch Size: 32
  - Learning Rate: 0.001
  - Early Stopping: ✅ Enabled
  - Patience: 10-15 epochs

### 3. Monitor Training
- Watch live logs and accuracy plot
- Training auto-stops when accuracy plateaus
- View KPI cards (Best Acc + Training Time)

### 4. Export Model
- Click **"EXPORT ONNX"** after training
- Use the exported model in production (C++/C#/Web/Mobile)

## 🎯 Achieving High Accuracy

The application includes **smart early stopping** that monitors validation accuracy (not loss), ensuring optimal performance:

| Setting | Value | Impact |
|---------|-------|--------|
| Model | ResNet50 | Best accuracy (85-95%) |
| Epochs | 30-50 | Sufficient convergence |
| Patience | 10-15 | Avoids premature stopping |
| Early Stopping | ✅ Enabled | Prevents overfitting |

**Result**: Consistently achieves **85%+ validation accuracy** on quality datasets.

## 🛠️ Building Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --name InspecNetPro --onedir --console --clean main.py

# Run executable
cd dist/InspecNetPro
./InspecNetPro.exe  # Windows
./InspecNetPro      # Linux/Mac
```

The executable will be in `dist/InspecNetPro/` folder.

## 📁 Project Structure

```
inspecnet-pro/
├── main.py                    # Main application entry point
├── src/
│   ├── dataset.py            # Dataset loading and preprocessing
│   ├── model.py              # Model factory (3 architectures)
│   ├── trainer.py            # Training logic with early stopping
│   ├── exporter.py           # ONNX export functionality
│   ├── ui_styles.py          # UI styling and themes
│   └── ui_components.py      # Custom Qt widgets
├── checkpoints/              # Saved model checkpoints (.pt)
├── model_exports/            # Exported ONNX models
├── docs/                     # Documentation and screenshots
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── QUICKSTART.md             # Quick start guide
└── LICENSE                   # MIT License
```

## 🔧 Technical Stack

- **GUI Framework**: PySide6 (Qt)
- **Deep Learning**: PyTorch 2.6.0 + CUDA
- **Visualization**: Matplotlib
- **Image Processing**: Pillow, NumPy
- **Model Export**: ONNX Runtime
- **Build Tool**: PyInstaller

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 3 steps
- [Full Documentation](docs/DOCUMENTATION.md) - Complete feature guide
- [Training Best Practices](docs/TRAINING_GUIDE.md) - Tips for high accuracy
- [API Reference](docs/API.md) - Code documentation

## 🐛 Troubleshooting

### Low Accuracy (<85%)
1. Increase epochs to 40-50
2. Increase patience to 15-20
3. Use ResNet50 model
4. Check dataset quality (balanced classes, clean labels)

### GPU Not Detected
1. Install NVIDIA CUDA Toolkit
2. Verify GPU with: `python -c "import torch; print(torch.cuda.is_available())"`

### Out of Memory
1. Reduce batch size to 16 or 8
2. Use MobileNetV2 (lighter model)

See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for more solutions.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- Qt/PySide6 for the GUI framework
- ONNX community for model export standards

## 📧 Contact

- **Author**: Vedang Bandi
- **Email**: bandivedang@gmail.com
- **GitHub**: [@yourusername](https://github.com/vedangbandi)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ using PyTorch and PySide6**
