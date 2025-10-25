# ============================================================
# 1️⃣ SETUP ENVIRONMENT
# ============================================================
!pip install ultralytics==8.3.0 tensorflow==2.17.0 opencv-python-headless==4.9.0.80 matplotlib pandas seaborn tensorboard --quiet

import os
import zipfile
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from ultralytics import YOLO
from IPython.display import display, Image

print("✅ Environment setup done! Torch version:", torch.__version__)

# ============================================================
# 2️⃣ EXTRACT DATASET
# ============================================================
zip_path = '/content/Wedtect Segmentation.v2i.yolov8-obb.zip'
extract_path = '/content/dataset'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"✅ Dataset extracted to: {extract_path}")
!ls /content/dataset

# ============================================================
# 3️⃣ CONFIGURE TPU (IF AVAILABLE)
# ============================================================
try:
    import torch_xla.core.xla_model as xm
    device = xm.xla_device()
    print("🚀 TPU detected:", device)
except ImportError:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"⚠️ TPU not available, using device: {device}")

# ============================================================
# 4️⃣ LOAD YOLOv8 OBB MODEL
# ============================================================
model = YOLO('yolov8n-obb.pt')
print("✅ YOLOv8 Oriented Bounding Box model loaded!")

# ============================================================
# 5️⃣ TRAINING WITH TENSORBOARD LOGGING
# ============================================================
%load_ext tensorboard
%tensorboard --logdir runs/obb

dataset_yaml = '/content/dataset/data.yaml'

results = model.train(
    data=dataset_yaml,
    epochs=100,          # Adjust if needed
    imgsz=640,
    batch=16,
    name='wedtect-obb-final',
    workers=2,
    device=device,
    project='runs/obb'
)

print("✅ Training completed!")

# ============================================================
# 6️⃣ EVALUATE MODEL PERFORMANCE
# ============================================================
metrics = model.val()
print("📊 Evaluation Results:")
print(metrics)

# ============================================================
# 7️⃣ PLOT TRAINING GRAPHS
# ============================================================
results_path = '/content/runs/obb/wedtect-obb-final/results.csv'

try:
    df = pd.read_csv(results_path)
    plt.figure(figsize=(10,6))
    sns.lineplot(x='epoch', y='train/box_loss', data=df, label='Box Loss')
    sns.lineplot(x='epoch', y='metrics/precision(B)', data=df, label='Precision')
    sns.lineplot(x='epoch', y='metrics/recall(B)', data=df, label='Recall')
    plt.title('📈 Training Metrics Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
except FileNotFoundError:
    print(f"⚠️ Could not find results.csv at {results_path}")

# ============================================================
# 8️⃣ INFERENCE ON TEST IMAGES
# ============================================================
test_images_path = '/content/dataset/test/images'

results = model.predict(
    source=test_images_path,
    save=True,
    imgsz=640,
    conf=0.25
)

print("✅ Inference completed! Check the prediction folder:")
!ls runs/obb/predict*

# Display first few predictions
if results and hasattr(results[0], 'save_dir'):
    pred_dir = results[0].save_dir
    print(f"📂 Predictions saved in: {pred_dir}")

    for i, file in enumerate(sorted(os.listdir(pred_dir))[:5]):
        if file.endswith(('.jpg', '.png')):
            display(Image(filename=os.path.join(pred_dir, file)))
else:
    print("⚠️ No prediction results found.")

# ============================================================
# 9️⃣ EXPORT TRAINED MODEL
# ============================================================
model_path = '/content/wedtect-obb-final.pt'
model.save(model_path)
print(f"💾 Model exported successfully to: {model_path}")

# ============================================================
# 🔟 ADDITIONAL TESTING (MANUAL IMAGES)
# ============================================================
# You can drop in a new image to test the model manually
# Example:
# uploaded = files.upload()
# for filename in uploaded.keys():
#     print(f"🧠 Running inference on {filename}")
#     results = model.predict(source=filename, save=True, imgsz=640, conf=0.3)
#     display(Image(filename=os.path.join(results[0].save_dir, filename)))
