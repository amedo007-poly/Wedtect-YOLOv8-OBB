"""
Image Scraper - Using iCrawler (PROVEN WORKING)
================================================
This uses Google Images through icrawler - reliable and tested
"""

import os
from pathlib import Path
import time
from PIL import Image
import io

def scrape_images_icrawler():
    """
    Download images using iCrawler (Google Images crawler)
    More reliable than Bing for this use case
    """
    
    try:
        from icrawler.builtin import GoogleImageCrawler
    except ImportError:
        print("❌ iCrawler not installed. Installing...")
        os.system('pip install icrawler -q')
        from icrawler.builtin import GoogleImageCrawler
    
    output_dir = Path('SCRAPED_IMAGES')
    output_dir.mkdir(exist_ok=True)
    
    search_config = {
        'crack': [
            'concrete crack damage',
            'structural crack wall',
            'surface crack defect',
            'pavement crack',
            'rock crack texture'
        ],
        'dent': [
            'metal dent damage surface',
            'car door dent',
            'panel dent defect',
            'impact dent mark',
            'surface dent texture'
        ],
        'hole': [
            'hole in surface metal',
            'corrosion hole damage',
            'material hole defect',
            'surface hole puncture',
            'structural hole'
        ],
        'leak': [
            'water leak damage stain',
            'pipe leak water',
            'roof leak damage',
            'moisture leak mark',
            'water stain leak'
        ]
    }
    
    total_downloaded = 0
    
    for defect_type, searches in search_config.items():
        defect_dir = output_dir / defect_type
        defect_dir.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"📥 Downloading {defect_type.upper()} images...")
        print(f"{'='*60}")
        
        downloaded_for_type = 0
        
        for search_query in searches:
            print(f"\n🔍 Searching: '{search_query}'")
            
            try:
                # Create crawler for this search
                google_crawler = GoogleImageCrawler(storage={'root_dir': str(defect_dir)})
                
                # Crawl images
                # num_images is approximate (Google limits per query)
                google_crawler.crawl(keyword=search_query, max_num=60)
                
                # Count downloaded images
                images_in_dir = len(list(defect_dir.glob('*.jpg'))) + len(list(defect_dir.glob('*.png')))
                
                print(f"  ✓ Downloaded for: {search_query}")
                print(f"  📊 Total in folder: {images_in_dir}")
                
                # Stop if we have enough
                if images_in_dir >= 250:
                    break
                
                # Rate limiting to avoid blocking
                time.sleep(1)
                    
            except Exception as e:
                print(f"  ⚠️  Error with '{search_query}': {str(e)[:100]}")
                continue
        
        final_count = len(list(defect_dir.glob('*.jpg'))) + len(list(defect_dir.glob('*.png')))
        print(f"\n✅ Total for {defect_type}: {final_count} images")
        total_downloaded += final_count
    
    print(f"\n\n{'='*60}")
    print(f"🎉 COMPLETE: Total {total_downloaded} images downloaded")
    print(f"{'='*60}")
    
    # Verify images
    verify_images(output_dir)
    
    return total_downloaded > 0


def verify_images(scraped_dir):
    """
    Verify downloaded images and clean up corrupt ones
    """
    print(f"\n🔍 Verifying images...")
    
    removed = 0
    
    for image_file in scraped_dir.rglob('*'):
        if image_file.is_file():
            try:
                # Try to open each image
                img = Image.open(image_file)
                img.verify()
            except Exception:
                # Remove corrupt images
                try:
                    image_file.unlink()
                    removed += 1
                except:
                    pass
    
    if removed > 0:
        print(f"  ⚠️  Removed {removed} corrupt images")
    else:
        print(f"  ✅ All images verified")


if __name__ == '__main__':
    print("="*60)
    print("🌐 Image Scraper - Google Images (iCrawler)")
    print("="*60)
    print("\nStarting image download...")
    print("This may take 10-15 minutes\n")
    
    try:
        success = scrape_images_icrawler()
        
        if success:
            print("\n✅ SUCCESS! Images downloaded to SCRAPED_IMAGES/")
            print("\nNext steps:")
            print("1. Review images in SCRAPED_IMAGES/ folder")
            print("2. Upload to Roboflow for annotation")
            print("3. See WORKFLOW_COMPLETE.md for details")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        print("\nTroubleshooting: Make sure you have:")
        print("  - pip install icrawler")
        print("  - pip install pillow")
