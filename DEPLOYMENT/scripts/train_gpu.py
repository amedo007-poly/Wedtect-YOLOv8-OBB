"""
YOLOv8 OBB Training Script for Wedtect - GPU Version
Optimized for NVIDIA GPUs (RTX 4070, etc.)
"""

import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
LOG_FILE = PROJECT_ROOT / "TRAINING_PROGRESS.txt"

def log_msg(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def main():
    """Main training function"""
    
    # Initialize log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("WEDTECT YOLOv8 OBB TRAINING LOG - GPU VERSION\n")
        f.write("="*70 + "\n\n")

    log_msg("🚀 Starting Wedtect YOLOv8 OBB Training on GPU")
    log_msg("=" * 70)

    try:
        # Step 1: Extract dataset
        log_msg("\n1️⃣  EXTRACTING DATASET")
        dataset_zip = PROJECT_ROOT / "Wedtect Segmentation.v2i.yolov8-obb.zip"
        dataset_dir = PROJECT_ROOT / "dataset"
        
        if not dataset_zip.exists():
            log_msg(f"❌ Dataset zip not found: {dataset_zip}")
            sys.exit(1)
        
        log_msg(f"Found dataset zip: {dataset_zip.name} ({dataset_zip.stat().st_size / (1024**2):.1f} MB)")
        
        if not dataset_dir.exists():
            log_msg(f"Extracting to: {dataset_dir}")
            with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
            log_msg("✅ Dataset extracted!")
        else:
            log_msg("✅ Dataset already extracted")
        
        # Step 2: Find data.yaml
        log_msg("\n2️⃣  LOCATING DATA.YAML")
        data_yaml_paths = list(dataset_dir.rglob("data.yaml"))
        
        if not data_yaml_paths:
            log_msg(f"❌ data.yaml not found in {dataset_dir}")
            sys.exit(1)
        
        data_yaml = data_yaml_paths[0]
        log_msg(f"✅ Found data.yaml: {data_yaml}")
        
        # Read and log yaml content
        with open(data_yaml, 'r') as f:
            yaml_content = f.read()
        
        log_msg(f"\nDataset YAML content:\n{yaml_content}")
        
        # Step 3: Import YOLOv8
        log_msg("\n3️⃣  IMPORTING YOLOv8")
        try:
            from ultralytics import YOLO
            import torch
            log_msg(f"✅ PyTorch version: {torch.__version__}")
            log_msg(f"✅ CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                log_msg(f"✅ GPU: {torch.cuda.get_device_name(0)}")
                log_msg(f"✅ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
                device = 0  # GPU device ID
            else:
                log_msg("⚠️  GPU not available, using CPU (training will be slow)")
                device = "cpu"
        except ImportError as e:
            log_msg(f"❌ Failed to import: {e}")
            sys.exit(1)
        
        # Step 4: Train model
        log_msg("\n4️⃣  STARTING TRAINING")
        log_msg("Loading YOLOv8 OBB model...")
        
        model = YOLO('yolov8n-obb.pt')
        log_msg("✅ Model loaded")
        
        log_msg("\n🚀 Beginning training on GPU...")
        log_msg("=" * 70)
        
        # Training with reduced workers to avoid multiprocessing issues on Windows
        results = model.train(
            data=str(data_yaml),
            epochs=100,
            imgsz=640,
            batch=16,
            device=device,
            workers=0,  # Set to 0 for Windows to avoid multiprocessing issues
            project=str(PROJECT_ROOT / "runs"),
            name='obb/wedtect-obb-final',
            patience=20,
            save=True,
            verbose=True,
            close_mosaic=10
        )
        
        log_msg("\n" + "=" * 70)
        log_msg("✅ TRAINING COMPLETED!")
        
        # Step 5: Results summary
        log_msg("\n5️⃣  RESULTS")
        results_path = PROJECT_ROOT / "runs" / "obb" / "wedtect-obb-final"
        best_model = results_path / "weights" / "best.pt"
        
        if best_model.exists():
            log_msg(f"✅ Best model saved: {best_model}")
            log_msg(f"   Size: {best_model.stat().st_size / (1024**2):.1f} MB")
        
        log_msg(f"✅ Results folder: {results_path}")
        log_msg(f"✅ Check: results.csv for metrics")
        log_msg(f"✅ Check: results.png for training graphs")
        log_msg(f"✅ Check: predict/ for test predictions")
        
        log_msg("\n🎉 TRAINING PIPELINE COMPLETE!")
        log_msg("=" * 70)

    except Exception as e:
        log_msg(f"\n❌ ERROR: {e}")
        import traceback
        log_msg(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
