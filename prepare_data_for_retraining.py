"""
Data Preparation for Retraining
================================
Merge scraped + annotated images with original training data.
Prepare everything for the retraining pipeline.

Usage:
    python prepare_data_for_retraining.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def merge_datasets(roboflow_dir, training_data_dir, backup=True):
    """
    Merge Roboflow-annotated images with original training data.
    
    Args:
        roboflow_dir: Path to Roboflow export directory
        training_data_dir: Path to TRAINING_DATA directory
        backup: Whether to backup original data first
    """
    
    roboflow_path = Path(roboflow_dir)
    training_path = Path(training_data_dir)
    
    print("=" * 70)
    print("🔄 MERGING DATASETS")
    print("=" * 70)
    
    # Backup original data
    if backup:
        print("\n📦 Backing up original data...")
        backup_dir = training_path.parent / f"TRAINING_DATA_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(training_path, backup_dir)
        print(f"✓ Backup created: {backup_dir}")
    
    # Merge for each split (train, val, test)
    splits = ['train', 'val', 'test']
    
    for split in splits:
        print(f"\n📋 Merging {split.upper()} data...")
        
        src_images = roboflow_path / split / 'images'
        src_labels = roboflow_path / split / 'labels'
        
        dst_images = training_path / split / 'images'
        dst_labels = training_path / split / 'labels'
        
        # Create directories if they don't exist
        dst_images.mkdir(parents=True, exist_ok=True)
        dst_labels.mkdir(parents=True, exist_ok=True)
        
        # Copy images
        if src_images.exists():
            image_count = 0
            for img_file in src_images.glob('*'):
                if img_file.is_file():
                    shutil.copy2(img_file, dst_images / img_file.name)
                    image_count += 1
            print(f"  ✓ Copied {image_count} images to {split}")
        
        # Copy labels
        if src_labels.exists():
            label_count = 0
            for label_file in src_labels.glob('*'):
                if label_file.is_file():
                    shutil.copy2(label_file, dst_labels / label_file.name)
                    label_count += 1
            print(f"  ✓ Copied {label_count} labels to {split}")
    
    print("\n✅ MERGE COMPLETE")


def verify_dataset(training_data_dir):
    """
    Verify dataset structure and counts.
    
    Args:
        training_data_dir: Path to TRAINING_DATA directory
    
    Returns:
        Dictionary with dataset statistics
    """
    
    training_path = Path(training_data_dir)
    
    print("\n" + "=" * 70)
    print("📊 DATASET VERIFICATION")
    print("=" * 70)
    
    stats = {}
    total_images = 0
    total_labels = 0
    
    for split in ['train', 'val', 'test']:
        split_path = training_path / split
        
        images_dir = split_path / 'images'
        labels_dir = split_path / 'labels'
        
        img_count = len(list(images_dir.glob('*'))) if images_dir.exists() else 0
        label_count = len(list(labels_dir.glob('*'))) if labels_dir.exists() else 0
        
        stats[split] = {
            'images': img_count,
            'labels': label_count
        }
        
        total_images += img_count
        total_labels += label_count
        
        print(f"\n{split.upper()}:")
        print(f"  Images: {img_count}")
        print(f"  Labels: {label_count}")
        print(f"  Match: {'✓ Yes' if img_count == label_count else '❌ No (MISMATCH!)'}")
    
    print(f"\n{'='*70}")
    print(f"📈 TOTAL:")
    print(f"  Total Images: {total_images}")
    print(f"  Total Labels: {total_labels}")
    print(f"  Overall Match: {'✓ Yes' if total_images == total_labels else '❌ No (CHECK MISMATCHES!)'}")
    print(f"{'='*70}")
    
    return stats


def update_data_yaml(data_yaml_path, training_data_dir):
    """
    Update data.yaml with correct paths and class information.
    
    Args:
        data_yaml_path: Path to data.yaml file
        training_data_dir: Path to TRAINING_DATA directory
    """
    
    print("\n✏️  Updating data.yaml...")
    
    # Read current data.yaml
    with open(data_yaml_path, 'r') as f:
        content = f.read()
    
    # Update paths (convert to absolute paths)
    training_path = Path(training_data_dir).absolute()
    
    new_content = f"""path: {training_path}
train: train/images
val: val/images
test: test/images

nc: 4  # Number of classes
names: ['crack', 'dent', 'hole', 'leak']
"""
    
    # Backup original
    backup_path = data_yaml_path.with_suffix('.yaml.bak')
    shutil.copy2(data_yaml_path, backup_path)
    
    # Write updated content
    with open(data_yaml_path, 'w') as f:
        f.write(new_content)
    
    print(f"✓ data.yaml updated")
    print(f"✓ Backup saved: {backup_path}")


def create_retraining_guide():
    """Create a guide for retraining with merged data."""
    
    guide = """
# 🚀 RETRAINING GUIDE

## After Dataset Merge

Your training data has been merged with new scraped + annotated images.

### 1. Verify Dataset Structure
```powershell
# Check that all images/labels match
dir TRAINING_DATA/train/images | measure-object -Line  # Count files
dir TRAINING_DATA/train/labels | measure-object -Line  # Should match above
```

### 2. Update Model Configuration
Edit your training script or use defaults:
```python
from ultralytics import YOLO

model = YOLO('DEPLOYMENT/model/best.pt')  # Load your trained model

results = model.train(
    data='TRAINING_DATA/data.yaml',
    epochs=50,           # Fine-tune for 50 epochs
    batch=16,
    device=0,            # GPU device
    patience=20,         # Early stopping
    imgsz=640,
    augment=True,        # Important for new data!
    mosaic=1.0,          # Image mosaic augmentation
    mixup=0.1,           # Mixup augmentation
    resume=True          # Resume from checkpoint
)
```

### 3. Start Retraining
```powershell
python train_gpu.py
# or use the command above directly in Python
```

### 4. Monitor Training
- Training will take 2-3 hours depending on dataset size
- Watch for improvements in precision/recall
- GPU will be utilized (RTX 4070)

### 5. Evaluate Results
```powershell
python evaluate_and_test.py
```

### 6. Compare Results
- Old Model: 83.92% precision, 86.06% recall
- New Model: Should show improvement!

---

## Expected Improvements

With 1000 additional annotated images:
- **Precision**: +2-5% improvement expected
- **Recall**: +3-7% improvement expected  
- **mAP@50**: +2-4% improvement expected
- **Generalization**: Significantly better

### Why Improvements Happen:
1. More training data reduces overfitting
2. Diverse examples improve robustness
3. Web-scraped images cover edge cases
4. Fine-tuning on new data strengthens model

---

## Troubleshooting Retraining

### Training is slower than expected
- Normal for larger dataset
- Consider reducing epochs if needed
- Use smaller batch size if memory-constrained

### No improvement in metrics
- Check data.yaml paths are correct
- Verify labels are properly formatted
- Try more epochs (75-100)
- Check for class imbalance

### Model crashes during training
- Reduce batch size: batch=8
- Reduce image size: imgsz=512
- Check GPU memory: nvidia-smi

---

## Next Steps After Retraining

1. Evaluate on test set
2. Compare old vs new model performance
3. Deploy new model to DEPLOYMENT/model/best.pt
4. Push to GitHub with updated metrics
5. Consider deploying to production

---

Good luck with your improved model! 🚀
"""
    
    return guide


if __name__ == '__main__':
    # Configuration
    ROBOFLOW_DIR = 'Roboflow_Output'  # Change this to your Roboflow export path
    TRAINING_DATA_DIR = 'TRAINING_DATA'
    DATA_YAML = Path(TRAINING_DATA_DIR) / 'data.yaml'
    
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║         DATA PREPARATION FOR RETRAINING                            ║
    ║                                                                    ║
    ║  This script merges Roboflow-annotated images with your           ║
    ║  original training data to prepare for retraining.                ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Step 1: Merge datasets
        if Path(ROBOFLOW_DIR).exists():
            merge_datasets(ROBOFLOW_DIR, TRAINING_DATA_DIR, backup=True)
        else:
            print(f"\n⚠️  Roboflow directory not found: {ROBOFLOW_DIR}")
            print("Please ensure you've downloaded and extracted Roboflow data first.")
        
        # Step 2: Verify dataset
        stats = verify_dataset(TRAINING_DATA_DIR)
        
        # Step 3: Update data.yaml
        if DATA_YAML.exists():
            update_data_yaml(DATA_YAML, TRAINING_DATA_DIR)
        
        # Step 4: Create guide
        guide = create_retraining_guide()
        guide_path = Path('RETRAINING_GUIDE.md')
        with open(guide_path, 'w') as f:
            f.write(guide)
        print(f"\n✓ Retraining guide created: {guide_path}")
        
        print("\n" + "=" * 70)
        print("✅ DATA PREPARATION COMPLETE!")
        print("=" * 70)
        print(f"\nNext step: Run training")
        print(f"  python train_gpu.py")
        print("\nOr follow the guide:")
        print(f"  {guide_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
