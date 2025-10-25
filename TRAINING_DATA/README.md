# 📦 WEDTECT YOLOv8 OBB - TRAINING DATA FOLDER

Original training dataset and training results.

## 📁 Folder Structure

```
TRAINING_DATA/
├── train/
│   ├── images/ (857 training images)
│   └── labels/ (857 corresponding labels)
├── valid/
│   ├── images/ (245 validation images)
│   └── labels/ (245 corresponding labels)
├── test/
│   ├── images/ (122 test images)
│   └── labels/ (122 corresponding labels)
├── data.yaml (dataset configuration)
├── results.csv (training metrics for all 100 epochs)
└── args.yaml (training hyperparameters)
```

## 📊 Dataset Statistics:

- **Source**: Wedtect Segmentation v2i (Roboflow)
- **Format**: YOLOv8 Oriented Bounding Box (OBB)
- **Total Images**: 1,224 (857 train + 245 val + 122 test)
- **Classes**: 4
  - 🟢 Crack
  - 🔴 Dent
  - 🔵 Hole
  - 🟠 Leak

## 📋 Files in This Folder:

### data.yaml
Dataset configuration file with:
- Paths to train/val/test image directories
- Class definitions (crack, dent, hole, leak)
- Used for both training and validation

### results.csv
Raw training data for all 100 epochs:
- Epoch number
- Training loss
- Validation loss
- Precision
- Recall
- mAP@50
- mAP@50-95
- And more metrics...

### args.yaml
Complete training configuration showing:
- Model: yolov8n-obb
- Epochs: 100
- Batch size: 16
- Image size: 640×640
- Learning rate: 0.01
- Device: CUDA:0 (RTX 4070)
- All hyperparameters used

## 🎯 Training Summary:

- **Model**: YOLOv8 Nano OBB
- **Training Time**: ~2.5-3 hours (on RTX 4070)
- **Total Epochs**: 100 (fully completed)
- **Final Precision**: 83.92%
- **Final Recall**: 86.06%
- **Final mAP@50**: 87.22%

## 📈 Dataset Composition:

| Split | Images | Purpose |
|-------|--------|---------|
| Train | 857 | Model training |
| Validation | 245 | Performance monitoring |
| Test | 122 | Final evaluation |

## 🔄 To Retrain or Fine-tune:

Use `args.yaml` to understand exact configuration:
```python
from ultralytics import YOLO

# Load existing model for fine-tuning
model = YOLO('DEPLOYMENT/model/best.pt')

# Fine-tune with new data
results = model.train(
    data='TRAINING_DATA/data.yaml',
    epochs=50,  # additional epochs
    batch=16,
    device=0
)
```

## ⚙️ Hyperparameters Used:

- **Optimizer**: AdamW (auto-selected)
- **Learning Rate**: 0.01 (initial)
- **Batch Size**: 16
- **Image Size**: 640×640
- **Augmentation**: RandomAugment enabled
- **Early Stopping**: Patience=20
- **AMP**: Automatic Mixed Precision enabled

---

**For the trained model**: See `../DEPLOYMENT/model/best.pt`  
**For evaluation results**: See `../RESULTS/`  
**For documentation**: See `../DOCUMENTATION/`

---

Status: ✅ Training Completed Successfully  
Last Updated: 2025-10-25
