# 🚀 WEDTECT YOLOv8 OBB - DEPLOYMENT FOLDER

## Quick Start for Production

This folder contains everything you need to deploy the trained model.

### 📁 Folder Structure

```
DEPLOYMENT/
├── model/
│   └── best.pt ⭐ THE TRAINED MODEL (use this!)
└── scripts/
    ├── evaluate_and_test.py (test on new images)
    └── train_gpu.py (retrain/fine-tune if needed)
```

### 🎯 To Use the Model:

```python
from ultralytics import YOLO

# Load model
model = YOLO('model/best.pt')

# Predict
results = model.predict('image.jpg', conf=0.5)

# View
results[0].show()
```

### 📊 Performance:
- **Precision**: 83.92% (reliable predictions)
- **Recall**: 86.06% (catches most defects)
- **mAP@50**: 87.22% (excellent accuracy)

### ⚙️ Configuration:
- Confidence threshold: `conf=0.5` (default, balanced)
- Adjust to `conf=0.7` for high precision (fewer false positives)
- Adjust to `conf=0.3` for high recall (catch more defects)

### 📚 For More Information:
See `../DOCUMENTATION/` folder for detailed guides and reports.

---

**Status**: ✅ Production Ready  
**Last Updated**: 2025-10-25
