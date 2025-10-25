"""
================================================================================
    WEDTECT YOLOv8 OBB TRAINING SCRIPT (Local Machine)
================================================================================
    Dataset: Wedtect Segmentation v2i (Roboflow - YOLOv8 OBB format)
    Model: YOLOv8 Nano OBB
    Training: 100 epochs with GPU acceleration
    
    This script is adapted from the original Colab notebook for local execution.
    All paths are configured for Windows machines.
================================================================================
"""

import os
import sys
import zipfile
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

# ============================================================
# CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).parent
DATASET_ZIP = PROJECT_ROOT / "Wedtect Segmentation.v2i.yolov8-obb.zip"
DATASET_DIR = PROJECT_ROOT / "dataset"
LOGS_DIR = PROJECT_ROOT / "logs"
RUNS_DIR = PROJECT_ROOT / "runs"
LOG_FILE = PROJECT_ROOT / "TRAINING_LOG.txt"

# Training parameters
EPOCHS = 100
IMG_SIZE = 640
BATCH_SIZE = 16
WORKERS = 4
PATIENCE = 20  # Early stopping patience

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def log_message(message, level="INFO"):
    """Log messages to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")


def print_header(title):
    """Print a formatted header"""
    header = f"\n{'='*70}\n{title}\n{'='*70}\n"
    log_message(header.strip())


def setup_environment():
    """Setup and verify the environment"""
    print_header("1️⃣  ENVIRONMENT SETUP")
    
    try:
        log_message(f"Python version: {sys.version}")
        log_message(f"PyTorch version: {torch.__version__}")
        log_message(f"CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            log_message(f"GPU: {torch.cuda.get_device_name(0)}")
            log_message(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            device = "cuda"
        else:
            log_message("⚠️  GPU not available, using CPU (training will be slower)")
            device = "cpu"
        
        log_message("✅ Environment setup complete!")
        return device
        
    except Exception as e:
        log_message(f"❌ Environment setup failed: {e}", "ERROR")
        sys.exit(1)


def extract_dataset():
    """Extract the Roboflow dataset"""
    print_header("2️⃣  DATASET EXTRACTION")
    
    try:
        if not DATASET_ZIP.exists():
            log_message(f"❌ Dataset zip not found: {DATASET_ZIP}", "ERROR")
            sys.exit(1)
        
        log_message(f"Dataset zip found: {DATASET_ZIP}")
        log_message(f"Zip file size: {DATASET_ZIP.stat().st_size / (1024**2):.2f} MB")
        
        # Create dataset directory
        DATASET_DIR.mkdir(exist_ok=True)
        
        # Extract zip
        log_message(f"Extracting dataset to: {DATASET_DIR}")
        with zipfile.ZipFile(DATASET_ZIP, 'r') as zip_ref:
            zip_ref.extractall(DATASET_DIR)
        
        # List extracted contents
        extracted_items = list(DATASET_DIR.iterdir())
        log_message(f"✅ Dataset extracted! Found {len(extracted_items)} items:")
        for item in extracted_items:
            log_message(f"   - {item.name}")
        
        return True
        
    except Exception as e:
        log_message(f"❌ Dataset extraction failed: {e}", "ERROR")
        sys.exit(1)


def validate_dataset():
    """Validate the dataset structure"""
    print_header("3️⃣  DATASET VALIDATION")
    
    try:
        # Find data.yaml (Roboflow puts it in root or specific folder)
        data_yaml_paths = list(DATASET_DIR.rglob("data.yaml"))
        
        if not data_yaml_paths:
            log_message("❌ data.yaml not found in dataset!", "ERROR")
            log_message("Dataset structure:")
            for root, dirs, files in os.walk(DATASET_DIR):
                level = root.replace(str(DATASET_DIR), '').count(os.sep)
                indent = ' ' * 2 * level
                log_message(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:10]:  # Limit to first 10 files
                    log_message(f"{subindent}{file}")
            sys.exit(1)
        
        data_yaml = data_yaml_paths[0]
        log_message(f"✅ Found data.yaml at: {data_yaml}")
        
        # Read and log yaml content
        with open(data_yaml, 'r') as f:
            yaml_content = f.read()
            log_message("YAML Configuration:")
            for line in yaml_content.split('\n'):
                if line.strip():
                    log_message(f"  {line}")
        
        # Count dataset splits
        for split in ['train', 'val', 'test']:
            split_path = DATASET_DIR / split / 'images'
            if split_path.exists():
                count = len(list(split_path.glob('*.*')))
                log_message(f"✅ {split.upper()}: {count} images found")
            else:
                log_message(f"⚠️  {split.upper()}: Not found at {split_path}")
        
        return str(data_yaml)
        
    except Exception as e:
        log_message(f"❌ Dataset validation failed: {e}", "ERROR")
        sys.exit(1)


def train_model(device, data_yaml):
    """Train the YOLOv8 OBB model"""
    print_header("4️⃣  MODEL TRAINING")
    
    try:
        log_message("Loading YOLOv8 Nano OBB model...")
        model = YOLO('yolov8n-obb.pt')
        log_message("✅ Model loaded successfully!")
        
        log_message(f"Training Configuration:")
        log_message(f"  - Epochs: {EPOCHS}")
        log_message(f"  - Image Size: {IMG_SIZE}x{IMG_SIZE}")
        log_message(f"  - Batch Size: {BATCH_SIZE}")
        log_message(f"  - Device: {device}")
        log_message(f"  - Workers: {WORKERS}")
        log_message(f"  - Early Stopping Patience: {PATIENCE}")
        log_message(f"  - Dataset YAML: {data_yaml}")
        
        log_message("\n🚀 Starting training... This may take several hours.")
        log_message("Monitor progress in the output below:\n")
        
        # Create runs directory
        RUNS_DIR.mkdir(exist_ok=True)
        
        # Train model
        results = model.train(
            data=data_yaml,
            epochs=EPOCHS,
            imgsz=IMG_SIZE,
            batch=BATCH_SIZE,
            device=device,
            workers=WORKERS,
            project=str(RUNS_DIR / "obb"),
            name='wedtect-obb-final',
            patience=PATIENCE,
            save=True,
            verbose=True,
            close_mosaic=10
        )
        
        log_message("\n✅ Training completed successfully!")
        return results
        
    except Exception as e:
        log_message(f"❌ Training failed: {e}", "ERROR")
        sys.exit(1)


def evaluate_model(model):
    """Evaluate the trained model"""
    print_header("5️⃣  MODEL EVALUATION")
    
    try:
        log_message("Running validation on validation dataset...")
        metrics = model.val()
        
        log_message("\n📊 Evaluation Metrics:")
        log_message(f"  - Box Loss: {metrics.box.mean():.4f}")
        log_message(f"  - Precision: {metrics.results_dict.get('metrics/precision(B)', 'N/A')}")
        log_message(f"  - Recall: {metrics.results_dict.get('metrics/recall(B)', 'N/A')}")
        log_message(f"  - mAP50: {metrics.results_dict.get('metrics/mAP50(B)', 'N/A')}")
        log_message(f"  - mAP50-95: {metrics.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")
        
        log_message("✅ Evaluation complete!")
        return metrics
        
    except Exception as e:
        log_message(f"⚠️  Evaluation had issues: {e}")
        return None


def plot_results():
    """Plot training results"""
    print_header("6️⃣  RESULTS VISUALIZATION")
    
    try:
        results_path = RUNS_DIR / "obb" / "wedtect-obb-final" / "results.csv"
        
        if not results_path.exists():
            log_message(f"⚠️  Results file not found: {results_path}", "WARNING")
            return
        
        log_message(f"Reading results from: {results_path}")
        df = pd.read_csv(results_path)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Wedtect YOLOv8 OBB Training Results', fontsize=16)
        
        # Plot 1: Box Loss
        axes[0, 0].plot(df['epoch'], df['train/box_loss'], label='Train', marker='o', markersize=3)
        axes[0, 0].plot(df['epoch'], df['val/box_loss'], label='Val', marker='s', markersize=3)
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].set_title('Box Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Precision & Recall
        if 'metrics/precision(B)' in df.columns and 'metrics/recall(B)' in df.columns:
            axes[0, 1].plot(df['epoch'], df['metrics/precision(B)'], label='Precision', marker='o', markersize=3)
            axes[0, 1].plot(df['epoch'], df['metrics/recall(B)'], label='Recall', marker='s', markersize=3)
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('Score')
            axes[0, 1].set_title('Precision & Recall')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: mAP
        if 'metrics/mAP50(B)' in df.columns:
            axes[1, 0].plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50', marker='o', markersize=3)
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('mAP50')
            axes[1, 0].set_title('Mean Average Precision')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Training Summary
        axes[1, 1].axis('off')
        summary_text = f"""
        Training Summary
        
        Total Epochs: {len(df)}
        Final Box Loss: {df['train/box_loss'].iloc[-1]:.4f}
        Best Epoch: {df['epoch'].idxmin() + 1}
        
        Dataset: Wedtect Segmentation v2i
        Model: YOLOv8 Nano OBB
        """
        axes[1, 1].text(0.1, 0.5, summary_text, fontsize=11, family='monospace', 
                       verticalalignment='center')
        
        plot_path = RUNS_DIR / "obb" / "wedtect-obb-final" / "training_plots.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        log_message(f"✅ Training plots saved to: {plot_path}")
        
        plt.close()
        
    except Exception as e:
        log_message(f"⚠️  Plot generation had issues: {e}")


def run_inference(model):
    """Run inference on test images"""
    print_header("7️⃣  INFERENCE TESTING")
    
    try:
        test_dir = DATASET_DIR / "test" / "images"
        
        if not test_dir.exists():
            log_message(f"⚠️  Test directory not found: {test_dir}")
            return
        
        test_images = list(test_dir.glob('*.*'))
        log_message(f"Found {len(test_images)} test images")
        
        if len(test_images) == 0:
            log_message("⚠️  No test images found")
            return
        
        log_message("Running inference on test images...")
        results = model.predict(
            source=str(test_dir),
            save=True,
            imgsz=IMG_SIZE,
            conf=0.25
        )
        
        log_message(f"✅ Inference complete! Generated {len(results)} predictions")
        
        # Find prediction folder
        predict_dirs = list(RUNS_DIR.rglob("predict*"))
        if predict_dirs:
            pred_dir = max(predict_dirs, key=os.path.getctime)
            log_message(f"✅ Predictions saved to: {pred_dir}")
            
            pred_images = list(pred_dir.glob('*.*'))
            log_message(f"   Found {len(pred_images)} prediction images")
        
    except Exception as e:
        log_message(f"⚠️  Inference had issues: {e}")


def export_model():
    """Export the trained model"""
    print_header("8️⃣  MODEL EXPORT")
    
    try:
        best_model_path = RUNS_DIR / "obb" / "wedtect-obb-final" / "weights" / "best.pt"
        
        if not best_model_path.exists():
            log_message(f"❌ Best model not found: {best_model_path}", "ERROR")
            return
        
        log_message(f"Loading best model from: {best_model_path}")
        model = YOLO(str(best_model_path))
        
        # Save final model
        final_model_path = PROJECT_ROOT / "wedtect-obb-final-trained.pt"
        import shutil
        shutil.copy(best_model_path, final_model_path)
        log_message(f"✅ Model exported to: {final_model_path}")
        
        # Log model info
        log_message("\nModel Information:")
        log_message(f"  - Path: {final_model_path}")
        log_message(f"  - Size: {final_model_path.stat().st_size / (1024**2):.2f} MB")
        log_message(f"  - Task: OBB (Oriented Bounding Box)")
        log_message(f"  - Framework: PyTorch")
        
        return final_model_path
        
    except Exception as e:
        log_message(f"❌ Model export failed: {e}", "ERROR")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main training pipeline"""
    
    # Clear log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("WEDTECT YOLOv8 OBB TRAINING LOG\n")
        f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
    
    log_message("🚀 Starting Wedtect YOLOv8 OBB Training Pipeline")
    
    try:
        # Step 1: Setup
        device = setup_environment()
        
        # Step 2: Extract dataset
        extract_dataset()
        
        # Step 3: Validate dataset
        data_yaml = validate_dataset()
        
        # Step 4: Train model
        results = train_model(device, data_yaml)
        
        # Step 5: Evaluate
        evaluate_model(YOLO(str(RUNS_DIR / "obb" / "wedtect-obb-final" / "weights" / "best.pt")))
        
        # Step 6: Visualize
        plot_results()
        
        # Step 7: Inference
        model = YOLO(str(RUNS_DIR / "obb" / "wedtect-obb-final" / "weights" / "best.pt"))
        run_inference(model)
        
        # Step 8: Export
        export_model()
        
        # Final summary
        print_header("✅ TRAINING PIPELINE COMPLETE!")
        log_message("\n📊 SUMMARY:")
        log_message(f"  - Project Root: {PROJECT_ROOT}")
        log_message(f"  - Dataset: {DATASET_DIR}")
        log_message(f"  - Runs/Results: {RUNS_DIR}")
        log_message(f"  - Log File: {LOG_FILE}")
        log_message(f"  - Training completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_message("\n🎉 All done! Check the log files and results directory for details.")
        
    except Exception as e:
        log_message(f"\n❌ FATAL ERROR: {e}", "CRITICAL")
        sys.exit(1)


if __name__ == "__main__":
    main()
