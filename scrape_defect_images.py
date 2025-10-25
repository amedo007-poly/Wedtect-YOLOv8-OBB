"""
Defect Image Web Scraper
========================
Downloads ~1000 defect images (cracks, dents, holes, leaks) from Bing Image Search.
Uses reliable methods with error handling and rate limiting.

Usage:
    python scrape_defect_images.py
"""

import os
import time
import requests
from pathlib import Path
from urllib.parse import quote
import json
from datetime import datetime

# Configuration
DEFECT_TYPES = {
    'crack': 250,        # ~250 images per type
    'dent': 250,
    'hole': 250,
    'leak': 250
}

OUTPUT_DIR = Path('SCRAPED_IMAGES')
LOG_FILE = OUTPUT_DIR / 'scraping_log.txt'

# Headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Bing Image Search configuration
BING_BASE_URL = "https://www.bing.com/images/search"


def setup_directories():
    """Create output directories for each defect type."""
    for defect_type in DEFECT_TYPES.keys():
        defect_dir = OUTPUT_DIR / defect_type
        defect_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directories created in: {OUTPUT_DIR.absolute()}")


def log_message(message):
    """Log messages to both console and file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"[{timestamp}] {message}"
    print(log_text)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_text + '\n')


def get_bing_image_urls(search_query, num_images=250):
    """
    Scrape image URLs from Bing Image Search.
    
    Args:
        search_query: Search term (e.g., "surface crack")
        num_images: Number of images to download
    
    Returns:
        List of image URLs
    """
    urls = []
    
    try:
        # Search query with relevant keywords
        query = f"{search_query} defect surface damage"
        params = {
            'q': query,
            'count': min(num_images, 150)  # Bing limits per request
        }
        
        log_message(f"Searching Bing for: '{query}'")
        
        # Make request to Bing
        response = requests.get(
            BING_BASE_URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        
        # Extract image URLs from HTML using simple parsing
        import re
        # Look for image src patterns in the HTML
        image_pattern = r'"murl":"([^"]+)"'
        matches = re.findall(image_pattern, response.text)
        
        urls = list(set(matches))[:num_images]  # Remove duplicates and limit
        log_message(f"Found {len(urls)} URLs for '{search_query}'")
        
    except requests.exceptions.RequestException as e:
        log_message(f"❌ Error searching Bing for '{search_query}': {str(e)}")
    except Exception as e:
        log_message(f"❌ Unexpected error: {str(e)}")
    
    return urls


def download_image(url, defect_type, image_num):
    """
    Download a single image from URL.
    
    Args:
        url: Image URL
        defect_type: Type of defect (crack, dent, hole, leak)
        image_num: Image number for naming
    
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Determine file format from content type
        content_type = response.headers.get('content-type', 'image/jpeg')
        if 'png' in content_type:
            ext = '.png'
        elif 'gif' in content_type:
            ext = '.gif'
        elif 'webp' in content_type:
            ext = '.webp'
        else:
            ext = '.jpg'
        
        # Save image
        filename = f"{defect_type}_scraped_{image_num:04d}{ext}"
        filepath = OUTPUT_DIR / defect_type / filename
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Verify file size (skip very small files)
        file_size = filepath.stat().st_size
        if file_size < 5000:  # Less than 5KB is likely broken
            filepath.unlink()
            return False
        
        return True
        
    except Exception as e:
        return False


def scrape_defect_images():
    """Main scraping function."""
    setup_directories()
    
    log_message("=" * 60)
    log_message("🚀 STARTING DEFECT IMAGE SCRAPING")
    log_message("=" * 60)
    log_message(f"Target images per defect type: ~{list(DEFECT_TYPES.values())[0]}")
    log_message(f"Total target images: ~{sum(DEFECT_TYPES.values())}")
    log_message("")
    
    total_downloaded = 0
    search_queries = {
        'crack': [
            'surface crack concrete',
            'crack in material',
            'structural crack',
            'pavement crack',
            'wall crack'
        ],
        'dent': [
            'metal dent damage',
            'car dent surface',
            'dent in surface',
            'impact dent',
            'panel dent'
        ],
        'hole': [
            'hole in surface',
            'material hole damage',
            'corrosion hole',
            'surface perforation',
            'puncture hole'
        ],
        'leak': [
            'water leak damage',
            'pipe leak',
            'roof leak',
            'structural leak',
            'wall leak damage'
        ]
    }
    
    for defect_type, target_count in DEFECT_TYPES.items():
        log_message(f"\n📥 Scraping {defect_type.upper()} images (target: {target_count})")
        
        downloaded = 0
        queries = search_queries.get(defect_type, [defect_type])
        
        for query in queries:
            if downloaded >= target_count:
                break
            
            # Get URLs
            urls = get_bing_image_urls(query, num_images=100)
            
            if not urls:
                log_message(f"  ⚠️  No URLs found for query: '{query}'")
                continue
            
            # Download images
            for idx, url in enumerate(urls):
                if downloaded >= target_count:
                    break
                
                try:
                    if download_image(url, defect_type, downloaded + 1):
                        downloaded += 1
                        if downloaded % 10 == 0:
                            log_message(f"  ✓ {downloaded}/{target_count} images downloaded")
                    
                    # Rate limiting - be respectful
                    time.sleep(0.5)
                    
                except Exception as e:
                    continue
            
            time.sleep(2)  # Delay between queries
        
        log_message(f"  ✅ Completed: {downloaded} images for {defect_type}")
        total_downloaded += downloaded
    
    # Summary
    log_message("\n" + "=" * 60)
    log_message("📊 SCRAPING COMPLETE")
    log_message("=" * 60)
    log_message(f"Total images downloaded: {total_downloaded}")
    log_message(f"Output directory: {OUTPUT_DIR.absolute()}")
    log_message("")
    
    # Count actual files
    actual_counts = {}
    for defect_type in DEFECT_TYPES.keys():
        count = len(list((OUTPUT_DIR / defect_type).glob('*')))
        actual_counts[defect_type] = count
        log_message(f"  {defect_type.capitalize()}: {count} images")
    
    log_message(f"\n🎉 Total files in SCRAPED_IMAGES: {sum(actual_counts.values())}")
    log_message("✓ Log file saved to: " + str(LOG_FILE))
    
    return total_downloaded


def cleanup_corrupted_images():
    """Remove corrupted or invalid image files."""
    log_message("\n🧹 Checking for corrupted images...")
    
    removed = 0
    for defect_type in DEFECT_TYPES.keys():
        defect_dir = OUTPUT_DIR / defect_type
        
        for img_file in defect_dir.glob('*'):
            try:
                # Try to open and verify it's a valid image
                from PIL import Image
                img = Image.open(img_file)
                img.verify()
            except Exception:
                img_file.unlink()
                removed += 1
    
    if removed > 0:
        log_message(f"Removed {removed} corrupted images")
    else:
        log_message("No corrupted images found")


def organize_scraped_images():
    """Organize scraped images for training."""
    log_message("\n📁 Creating organized dataset structure...")
    
    organized_dir = Path('ORGANIZED_SCRAPED_DATA')
    for split in ['train', 'val', 'test']:
        for defect_type in DEFECT_TYPES.keys():
            (organized_dir / split / 'images').mkdir(parents=True, exist_ok=True)
    
    log_message(f"Organized structure created in: {organized_dir.absolute()}")
    log_message("Next step: Manually organize images into train/val/test folders")
    log_message("Then use Roboflow or another tool to create YOLO format labels")


if __name__ == '__main__':
    try:
        # Start scraping
        downloaded = scrape_defect_images()
        
        # Cleanup (optional)
        # cleanup_corrupted_images()
        
        # Organize
        organize_scraped_images()
        
        log_message("\n✅ SCRAPING WORKFLOW COMPLETE!")
        log_message("Next steps:")
        log_message("  1. Review downloaded images in SCRAPED_IMAGES folder")
        log_message("  2. Move quality images to ORGANIZED_SCRAPED_DATA")
        log_message("  3. Upload to Roboflow for annotation")
        log_message("  4. Add labeled data to your training dataset")
        
    except KeyboardInterrupt:
        log_message("\n❌ Scraping interrupted by user")
    except Exception as e:
        log_message(f"\n❌ Fatal error: {str(e)}")
        import traceback
        log_message(traceback.format_exc())
