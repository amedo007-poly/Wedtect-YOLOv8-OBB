"""
📊 IMAGE VIEWER - View all generated evaluation graphs
"""

from pathlib import Path
import subprocess
import os

def open_images():
    """Open all generated evaluation images"""
    
    eval_dir = Path("evaluation")
    
    if not eval_dir.exists():
        print("❌ Evaluation directory not found")
        return
    
    print("\n" + "="*70)
    print("📊 OPENING GENERATED EVALUATION GRAPHS...")
    print("="*70)
    
    # List all PNG files
    png_files = list(eval_dir.glob("*.png"))
    
    print(f"\n📁 Found {len(png_files)} graph files:")
    for i, png_file in enumerate(png_files, 1):
        print(f"  {i}. {png_file.name}")
    
    # Open images with default viewer
    for png_file in png_files:
        try:
            print(f"\n🔍 Opening: {png_file.name}")
            os.startfile(str(png_file.absolute()))
        except Exception as e:
            print(f"  ⚠️ Could not open: {e}")
    
    # Also open test predictions folder
    test_pred_dir = eval_dir / "test_predictions"
    if test_pred_dir.exists():
        print(f"\n📷 Opening test predictions folder...")
        try:
            os.startfile(str(test_pred_dir.absolute()))
        except Exception as e:
            print(f"  ⚠️ Could not open: {e}")
    
    print("\n" + "="*70)
    print("✅ All images are now open in your default viewer!")
    print("="*70 + "\n")

if __name__ == "__main__":
    open_images()
