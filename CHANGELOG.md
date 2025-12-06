# Changelog

All notable changes to InspecNet Pro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-12-06

### 🔧 Fixed
- **Critical**: Early stopping now monitors validation **accuracy** instead of loss
  - Previous behavior: Stopped at 73.9% accuracy
  - New behavior: Achieves 85%+ accuracy consistently
- Increased default patience from 5 to 10 epochs for better convergence

### ✨ Added
- KPI cards showing Best Validation Accuracy and Training Time
- Tooltips on all training controls for better UX
- Visual frame around early stopping controls with glassmorphism effect
- Training time tracking and display (formatted as "Xm Ys")
- Success log message when new best accuracy is achieved

### 🎨 Changed
- Default epochs: 10 → 20
- Default patience: 5 → 10 epochs
- Patience range: 1-30 → 3-30 (prevents too-early stopping)
- Improved header styling with cyan color
- Enhanced early stopping checkbox with bold cyan text

### 📚 Documentation
- Added comprehensive README.md for GitHub
- Created QUICKSTART.md for new users
- Added DELIVERY_SUMMARY.md with complete feature list
- Created LAUNCH_GUIDE.md for executable users

## [2.1.0] - 2025-12-05

### ✨ Added
- Abort Training button to cancel training mid-process
- Early stopping frame with visual styling
- Status pill updates for abort state

### 🎨 Changed
- Improved button styling with hover effects
- Better state management for training controls

## [2.0.0] - 2025-12-05

### ✨ Added
- Early stopping feature with configurable patience
- ONNX model export functionality
- User-customizable hyperparameters (epochs, batch size, learning rate)
- Export button with file dialog

### 🔧 Fixed
- Thread safety for UI updates using Qt.QueuedConnection
- QTextCursor.End attribute error

## [1.0.0] - 2025-12-05

### ✨ Initial Release
- Dataset loading with visual preview
- 3 model architectures (MobileNetV2, ResNet50, EfficientNetB0)
- Real-time training monitoring
- Live accuracy plot (train vs validation)
- Global progress bar
- Live console logs
- Inference page for predictions
- GPU auto-detection
- Professional dark UI with glassmorphism

### 🛠️ Technical
- PySide6 (Qt) GUI framework
- PyTorch 2.6.0 with CUDA support
- Matplotlib for visualization
- Data augmentation (ColorJitter, RandomHorizontalFlip)
- Learning rate scheduler (ReduceLROnPlateau)
- Gradient clipping for stability

---

## Legend

- ✨ Added: New features
- 🔧 Fixed: Bug fixes
- 🎨 Changed: Changes in existing functionality
- 🗑️ Deprecated: Soon-to-be removed features
- 🚀 Removed: Removed features
- 🔒 Security: Security fixes
- 📚 Documentation: Documentation changes
