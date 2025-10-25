"""
Monitor Scraper Progress
========================
Real-time progress tracker for image downloading
"""

import time
from pathlib import Path
from datetime import datetime

def monitor_scraper():
    """Monitor scraper progress in real-time"""
    
    scraped_dir = Path('SCRAPED_IMAGES')
    defect_types = ['crack', 'dent', 'hole', 'leak']
    
    print("\n" + "="*60)
    print("📊 SCRAPER PROGRESS MONITOR")
    print("="*60)
    print("Press Ctrl+C to stop monitoring\n")
    
    start_time = time.time()
    last_count = 0
    
    try:
        while True:
            # Count images per type
            counts = {}
            total = 0
            
            for defect_type in defect_types:
                defect_path = scraped_dir / defect_type
                count = len(list(defect_path.glob('*')))
                counts[defect_type] = count
                total += count
            
            # Calculate statistics
            elapsed = int(time.time() - start_time)
            rate = total / max(elapsed, 1)
            
            # Display progress
            print(f"\r⏱️  Time: {elapsed}s | Total: {total:3d} images | Rate: {rate:.1f} img/s", end='')
            
            # Show breakdown
            details = " | ".join([f"{t.upper()}: {counts[t]:3d}" for t in defect_types])
            print(f"\n   {details}", end='')
            
            # Estimate remaining time
            target = 1000
            remaining = target - total
            if rate > 0:
                eta_secs = remaining / rate
                eta_mins = int(eta_secs / 60)
                print(f" | ETA: {eta_mins}m for 1000 images")
            else:
                print()
            
            # Check if complete
            if total >= 1000:
                print(f"\n\n🎉 SUCCESS! Downloaded {total} images!")
                break
            
            last_count = total
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Monitoring stopped")
        print(f"Images downloaded so far: {total}")


if __name__ == '__main__':
    monitor_scraper()
