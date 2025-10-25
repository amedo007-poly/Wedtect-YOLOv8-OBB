"""
Monitor YOLOv8 Training Progress
Real-time tracking of GPU training on Wedtect dataset
"""
import os
import time
from pathlib import Path

def get_latest_results():
    """Get the latest training results file"""
    runs_dir = Path("runs/obb")
    if not runs_dir.exists():
        return None
    
    # Find the latest numbered directory
    obb_dirs = sorted([d for d in runs_dir.glob("wedtect-obb-final*") if d.is_dir()])
    if not obb_dirs:
        return None
    
    latest_dir = obb_dirs[-1]
    results_file = latest_dir / "results.csv"
    
    if results_file.exists():
        return results_file
    return None

def show_latest_epoch():
    """Show the latest epoch metrics"""
    results_file = get_latest_results()
    
    if not results_file:
        print("⏳ Training not started yet or results file not found...")
        return False
    
    try:
        with open(results_file, 'r') as f:
            lines = f.readlines()
        
        if len(lines) > 1:
            # Skip header, get last line
            latest = lines[-1].strip()
            header = lines[0].strip()
            
            print("\n" + "="*80)
            print("📊 LATEST TRAINING EPOCH")
            print("="*80)
            print(header)
            print(latest)
            
            # Extract epoch number
            cols = latest.split()
            if len(cols) > 0:
                epoch = cols[0]
                print(f"\n✅ Currently on Epoch: {epoch}")
            return True
        else:
            print("⏳ Waiting for first epoch to complete...")
            return False
    except Exception as e:
        print(f"⚠️  Could not read results: {e}")
        return False

def main():
    print("\n" + "🔍 WEDTECT YOLOv8 OBB TRAINING MONITOR")
    print("📍 Checking GPU training progress...")
    
    # Check if training is still running
    run_dir = Path("runs/obb")
    obb_dirs = sorted([d for d in run_dir.glob("wedtect-obb-final*") if d.is_dir()])
    
    if obb_dirs:
        latest_dir = obb_dirs[-1]
        print(f"\n📁 Training Directory: {latest_dir.name}")
        
        # Check for weights
        if (latest_dir / "weights").exists():
            weights = list((latest_dir / "weights").glob("*.pt"))
            if weights:
                print(f"💾 Checkpoints: {len(weights)} weight files found")
        
        show_latest_epoch()
        
        # Show estimated time remaining
        results_file = get_latest_results()
        if results_file:
            try:
                with open(results_file, 'r') as f:
                    lines = f.readlines()
                
                if len(lines) > 1:
                    epoch_num = int(lines[-1].split()[0])
                    remaining = 100 - epoch_num
                    # Rough estimate: ~1-2 min per epoch on RTX 4070
                    est_time_min = remaining * 1.5
                    hours = int(est_time_min // 60)
                    mins = int(est_time_min % 60)
                    
                    if remaining > 0:
                        print(f"\n⏱️  Estimated Time Remaining: ~{hours}h {mins}m ({remaining} epochs left)")
            except:
                pass
    else:
        print("⏳ No training directory found yet. Training may be initializing...")
    
    print("\n💡 Tip: Run this script again to check progress!")

if __name__ == "__main__":
    main()
