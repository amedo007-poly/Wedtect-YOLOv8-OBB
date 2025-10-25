"""
🎯 WEDTECT YOLOv8 OBB - EVALUATION & TESTING
Comprehensive analysis with prediction graphs, precision metrics, and inference testing
"""

import os
import sys
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from ultralytics import YOLO
import warnings
warnings.filterwarnings('ignore')

# Colors for visualization
COLORS = {
    'crack': (0, 255, 0),      # Green
    'dent': (255, 0, 0),       # Red
    'hole': (0, 0, 255),       # Blue
    'leak': (255, 165, 0)      # Orange
}

CLASS_NAMES = {0: 'crack', 1: 'dent', 2: 'hole', 3: 'leak'}

def log_msg(msg, level="ℹ️"):
    """Print formatted log message"""
    print(f"\n[{level}] {msg}")

def generate_training_curves():
    """Generate comprehensive training metrics visualization"""
    log_msg("Generating Training Curves and Metrics Graphs...", "📊")
    
    results_file = Path("runs/obb/wedtect-obb-final4/results.csv")
    
    if not results_file.exists():
        log_msg(f"Results file not found: {results_file}", "⚠️")
        return False
    
    try:
        df = pd.read_csv(results_file)
        
        # Create comprehensive figure with multiple subplots
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('YOLOv8 OBB Training Metrics - Wedtect Dataset', fontsize=16, fontweight='bold')
        
        # 1. Train vs Validation Loss
        if 'train/loss' in df.columns and 'val/loss' in df.columns:
            axes[0, 0].plot(df['train/loss'], label='Train Loss', linewidth=2)
            axes[0, 0].plot(df['val/loss'], label='Val Loss', linewidth=2)
            axes[0, 0].set_title('Training vs Validation Loss', fontweight='bold')
            axes[0, 0].set_xlabel('Epoch')
            axes[0, 0].set_ylabel('Loss')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Box Loss, DFL Loss, Cls Loss
        if 'train/box_loss' in df.columns:
            axes[0, 1].plot(df['train/box_loss'], label='Box Loss', linewidth=2)
            axes[0, 1].plot(df['train/dfl_loss'], label='DFL Loss', linewidth=2)
            axes[0, 1].plot(df['train/cls_loss'], label='Class Loss', linewidth=2)
            axes[0, 1].set_title('Component Losses Over Time', fontweight='bold')
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('Loss Value')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Precision Curve
        if 'metrics/precision(B)' in df.columns:
            axes[1, 0].plot(df['metrics/precision(B)'], color='green', linewidth=2, marker='o', markersize=4)
            axes[1, 0].set_title('Precision Over Epochs', fontweight='bold')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Precision')
            axes[1, 0].set_ylim([0, 1])
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Recall Curve
        if 'metrics/recall(B)' in df.columns:
            axes[1, 1].plot(df['metrics/recall(B)'], color='blue', linewidth=2, marker='o', markersize=4)
            axes[1, 1].set_title('Recall Over Epochs', fontweight='bold')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Recall')
            axes[1, 1].set_ylim([0, 1])
            axes[1, 1].grid(True, alpha=0.3)
        
        # 5. mAP50 Curve
        if 'metrics/mAP50(B)' in df.columns:
            axes[2, 0].plot(df['metrics/mAP50(B)'], color='red', linewidth=2, marker='s', markersize=4)
            axes[2, 0].set_title('mAP@50 Over Epochs', fontweight='bold')
            axes[2, 0].set_xlabel('Epoch')
            axes[2, 0].set_ylabel('mAP@50')
            axes[2, 0].set_ylim([0, 1])
            axes[2, 0].grid(True, alpha=0.3)
        
        # 6. mAP50-95 Curve
        if 'metrics/mAP50-95(B)' in df.columns:
            axes[2, 1].plot(df['metrics/mAP50-95(B)'], color='purple', linewidth=2, marker='d', markersize=4)
            axes[2, 1].set_title('mAP@50-95 Over Epochs', fontweight='bold')
            axes[2, 1].set_xlabel('Epoch')
            axes[2, 1].set_ylabel('mAP@50-95')
            axes[2, 1].set_ylim([0, 1])
            axes[2, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = Path("evaluation/training_metrics_detailed.png")
        output_path.parent.mkdir(exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        log_msg(f"✅ Training metrics graph saved: {output_path}", "✅")
        plt.close()
        
        return True
    except Exception as e:
        log_msg(f"Error generating training curves: {e}", "❌")
        return False

def generate_summary_stats():
    """Display training summary statistics"""
    log_msg("Extracting Final Training Statistics...", "📈")
    
    results_file = Path("runs/obb/wedtect-obb-final4/results.csv")
    
    try:
        df = pd.read_csv(results_file)
        
        last_row = df.iloc[-1]
        
        stats = {
            'Total Epochs': len(df),
            'Final Train Loss': float(last_row.get('train/loss', 0)),
            'Final Val Loss': float(last_row.get('val/loss', 0)),
            'Final Precision': float(last_row.get('metrics/precision(B)', 0)),
            'Final Recall': float(last_row.get('metrics/recall(B)', 0)),
            'Final mAP@50': float(last_row.get('metrics/mAP50(B)', 0)),
            'Final mAP@50-95': float(last_row.get('metrics/mAP50-95(B)', 0)),
        }
        
        print("\n" + "="*60)
        print("📊 TRAINING SUMMARY STATISTICS")
        print("="*60)
        for key, value in stats.items():
            if 'Loss' in key or 'Precision' in key or 'Recall' in key or 'mAP' in key:
                print(f"  {key:.<40} {value:.4f}")
            else:
                print(f"  {key:.<40} {value}")
        print("="*60)
        
        return stats
    except Exception as e:
        log_msg(f"Error extracting stats: {e}", "❌")
        return {}

def run_inference_on_test_set():
    """Run inference on test images and generate visualization"""
    log_msg("Running Inference on Test Set...", "🔍")
    
    # Find the best model
    model_path = Path("runs/obb/wedtect-obb-final4/weights/best.pt")
    
    if not model_path.exists():
        log_msg(f"Model not found: {model_path}", "❌")
        return False
    
    try:
        # Load model
        model = YOLO(str(model_path))
        log_msg(f"Model loaded: {model_path}", "✅")
        
        # Find test images
        test_dir = Path("dataset/test/images")
        if not test_dir.exists():
            log_msg(f"Test directory not found: {test_dir}", "⚠️")
            return False
        
        test_images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
        
        if not test_images:
            log_msg("No test images found", "⚠️")
            return False
        
        log_msg(f"Found {len(test_images)} test images", "ℹ️")
        
        # Run predictions on all test images
        output_dir = Path("evaluation/test_predictions")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        all_predictions = []
        
        for idx, img_path in enumerate(test_images[:20], 1):  # First 20 for visualization
            print(f"  Processing: {idx}/{min(20, len(test_images))} - {img_path.name}", end='\r')
            
            results = model.predict(str(img_path), conf=0.3, verbose=False)
            
            # Draw predictions
            img = cv2.imread(str(img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            for result in results:
                if result.obb is not None:
                    boxes = result.obb.cpu() if hasattr(result.obb, 'cpu') else result.obb
                    for i, box in enumerate(boxes.data):
                        # OBB format: [x, y, w, h, angle, conf, cls] or similar
                        # Let's check the structure first
                        box_data = box.cpu().numpy() if hasattr(box, 'cpu') else np.array(box)
                        
                        if len(box_data) >= 7:
                            # Standard OBB: x, y, width, height, angle, conf, cls
                            x, y, w, h, angle, conf, cls = box_data[:7]
                            class_name = CLASS_NAMES.get(int(cls), 'unknown')
                            color = COLORS.get(class_name, (255, 255, 255))
                            
                            # Draw rotated rectangle
                            center = (int(x), int(y))
                            size = (int(w), int(h))
                            angle_deg = float(angle)
                            
                            # Get rotated box corners
                            rect = cv2.RotatedRect(center, size, angle_deg)
                            pts = cv2.boxPoints(rect)
                            pts = np.int32(pts)
                            
                            cv2.polylines(img_rgb, [pts], True, color, 2)
                            
                            # Draw label
                            centroid = (int(x), int(y))
                            cv2.putText(img_rgb, f"{class_name} {conf:.2f}", 
                                       centroid, cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.5, color, 2)
                            
                            all_predictions.append({
                                'image': img_path.name,
                                'class': class_name,
                                'confidence': float(conf)
                            })
            
            # Save annotated image
            output_path = output_dir / f"pred_{img_path.stem}.jpg"
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(output_path), img_bgr)
        
        print()
        log_msg(f"Test predictions saved to: {output_dir}", "✅")
        
        # Create prediction statistics
        if all_predictions:
            pred_df = pd.DataFrame(all_predictions)
            pred_df.to_csv(output_dir / "predictions_summary.csv", index=False)
            
            print("\n" + "="*60)
            print("🎯 PREDICTION STATISTICS")
            print("="*60)
            print(f"  Total Detections: {len(pred_df)}")
            print(f"  Images Processed: {pred_df['image'].nunique()}")
            print("\n  Detections by Class:")
            for cls_name, count in pred_df['class'].value_counts().items():
                avg_conf = pred_df[pred_df['class'] == cls_name]['confidence'].mean()
                print(f"    {cls_name:.<20} {count:>3} detections (avg conf: {avg_conf:.3f})")
            print("="*60)
        
        return True
    except Exception as e:
        log_msg(f"Error running inference: {e}", "❌")
        import traceback
        traceback.print_exc()
        return False

def create_prediction_distribution_chart():
    """Create charts showing class distribution in predictions"""
    log_msg("Creating Prediction Distribution Charts...", "📊")
    
    pred_file = Path("evaluation/test_predictions/predictions_summary.csv")
    
    if not pred_file.exists():
        log_msg("Predictions file not found", "⚠️")
        return False
    
    try:
        pred_df = pd.read_csv(pred_file)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Test Set Prediction Analysis', fontsize=14, fontweight='bold')
        
        # Class distribution
        class_counts = pred_df['class'].value_counts()
        colors_list = [COLORS.get(cls_name, (100, 100, 100)) for cls_name in class_counts.index]
        colors_list = [(r/255, g/255, b/255) for r, g, b in colors_list]
        
        axes[0].bar(class_counts.index, class_counts.values, color=colors_list, alpha=0.7, edgecolor='black', linewidth=2)
        axes[0].set_title('Detections by Class', fontweight='bold')
        axes[0].set_xlabel('Class')
        axes[0].set_ylabel('Number of Detections')
        axes[0].grid(axis='y', alpha=0.3)
        
        # Confidence distribution
        for cls_name in pred_df['class'].unique():
            confidences = pred_df[pred_df['class'] == cls_name]['confidence']
            color = COLORS.get(cls_name, (100, 100, 100))
            color_rgb = tuple(c/255 for c in color)
            axes[1].hist(confidences, alpha=0.5, label=cls_name, bins=10, color=color_rgb, edgecolor='black')
        
        axes[1].set_title('Confidence Distribution', fontweight='bold')
        axes[1].set_xlabel('Confidence Score')
        axes[1].set_ylabel('Frequency')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        output_path = Path("evaluation/prediction_analysis.png")
        output_path.parent.mkdir(exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        log_msg(f"Prediction analysis saved: {output_path}", "✅")
        plt.close()
        
        return True
    except Exception as e:
        log_msg(f"Error creating prediction charts: {e}", "❌")
        return False

def main():
    """Main evaluation pipeline"""
    print("\n" + "="*70)
    print("🚀 WEDTECT YOLOv8 OBB - COMPREHENSIVE EVALUATION & TESTING")
    print("="*70)
    
    # Step 1: Generate training curves
    generate_training_curves()
    
    # Step 2: Print summary statistics
    stats = generate_summary_stats()
    
    # Step 3: Run inference on test set
    run_inference_on_test_set()
    
    # Step 4: Create prediction charts
    create_prediction_distribution_chart()
    
    print("\n" + "="*70)
    print("✅ EVALUATION COMPLETE!")
    print("="*70)
    print("\n📁 Generated Files:")
    print("  📊 evaluation/training_metrics_detailed.png - Training curves")
    print("  🎯 evaluation/test_predictions/ - Test predictions with visualizations")
    print("  📈 evaluation/prediction_analysis.png - Prediction statistics")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
