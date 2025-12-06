# Quick Start Guide - InspecNet Pro

## 🚀 Getting Started in 3 Steps

### Step 1: Load Your Dataset
1. Click **"Dataset"** tab in the sidebar
2. Click **"Browse"** and select your dataset folder
3. Click **"Load Dataset"**
4. Verify the dataset preview shows your images

**Dataset Structure:**
```
your_dataset/
├── class1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── class2/
│   ├── image1.jpg
│   └── ...
└── class3/
    └── ...
```

### Step 2: Configure Training
1. Click **"Training"** tab
2. **Recommended Settings for High Accuracy (85%+)**:
   - **Architecture**: ResNet50 (best accuracy) or MobileNetV2 (faster)
   - **Epochs**: 30-50
   - **Batch Size**: 32 (or 16 if GPU memory error)
   - **Learning Rate**: 0.001
   - **Early Stopping**: ✅ Enabled
   - **Patience**: 10-15 epochs

3. Click **"START TRAINING"**

### Step 3: Monitor & Export
1. Watch the **live logs** and **accuracy plot**
2. Training auto-stops when accuracy plateaus (if early stopping enabled)
3. After training completes:
   - Check **"Best Acc"** KPI card
   - Click **"EXPORT ONNX"** to save the model

---

## ⚙️ Advanced Features

### Early Stopping
- **Purpose**: Prevents overfitting, saves time
- **How it works**: Stops training if validation accuracy doesn't improve for N epochs
- **When to disable**: If you want to train for exact number of epochs

### Abort Training
- Click **"ABORT TRAINING"** to stop mid-process
- Useful if you see accuracy isn't improving

### Model Export (ONNX)
- **What**: Universal model format
- **Why**: Deploy anywhere (C++, web, mobile)
- **How**: Click "EXPORT ONNX" after training

---

## 🎯 Achieving 85%+ Accuracy

### If Accuracy is Low (<75%)
1. ✅ **Increase Epochs**: Try 40-50 epochs
2. ✅ **Increase Patience**: Set to 15-20 epochs
3. ✅ **Better Model**: Use ResNet50 instead of MobileNetV2
4. ✅ **Check Dataset**: Ensure balanced classes and clean labels
5. ✅ **Lower Learning Rate**: Try 0.0005 or 0.0001

### If Training is Too Slow
1. ✅ **Smaller Model**: Use MobileNetV2
2. ✅ **Reduce Batch Size**: Try 16 or 8
3. ✅ **Enable Early Stopping**: Avoids unnecessary epochs

### If Early Stopping Triggers Too Soon
1. ✅ **Increase Patience**: 15-20 epochs
2. ✅ **Check Plot**: Is accuracy still improving?
3. ✅ **Reduce Learning Rate**: 0.0005 for smoother convergence

---

## 📊 Understanding the UI

### KPI Cards
- **Best Acc**: Highest validation accuracy achieved
- **Time**: Total training duration

### Status Pill
- 🔵 **IDLE**: Ready to train
- 🟡 **TRAINING**: Training in progress
- 🟢 **COMPLETE**: Training finished successfully
- 🔴 **ERROR**: Something went wrong

### Progress Bar
- Shows overall progress across all epochs
- Caps at 99% until final epoch completes

### Live Logs
- Real-time training updates
- Color-coded messages:
  - ✓ Green: Success/improvement
  - ⚠️ Yellow: Warnings
  - ❌ Red: Errors

---

## 🐛 Common Issues

### "Load Dataset First" Error
**Solution**: Go to Dataset tab and load your data first

### GPU Out of Memory
**Solution**: Reduce batch size to 16 or 8

### Accuracy Stuck at ~70%
**Solution**: 
1. Increase epochs to 40-50
2. Increase patience to 15
3. Try ResNet50 model

### Training Takes Too Long
**Solution**: 
1. Enable early stopping
2. Use MobileNetV2
3. Reduce epochs to 20

---

## 💡 Pro Tips

1. **Always enable early stopping** with patience ≥ 10
2. **Start with 30 epochs** for most datasets
3. **Use ResNet50** for maximum accuracy
4. **Monitor the plot** - if accuracy plateaus, training will auto-stop
5. **Export to ONNX** for production deployment

---

## 📞 Need Help?

Check the full documentation: `README_TRAINING.md`

Happy Training! 🎉
