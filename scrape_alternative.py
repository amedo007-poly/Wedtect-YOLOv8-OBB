"""
Alternative: Using Bing-Image-Downloader Library
================================================
More reliable for web scraping with built-in error handling.

This script uses bing-image-downloader which is more robust and handles:
- Rate limiting automatically
- Error recovery
- Parallel downloads
- Image verification
"""

import os
from pathlib import Path
from datetime import datetime

# This requires: pip install bing-image-downloader


def scrape_with_bing_downloader():
    """
    Download images using bing-image-downloader library.
    
    Installation:
        pip install bing-image-downloader
    """
    
    try:
        from bing_image_downloader import downloader
    except ImportError:
        print("❌ bing-image-downloader not installed")
        print("Install it with: pip install bing-image-downloader")
        return False
    
    output_dir = Path('SCRAPED_IMAGES')
    output_dir.mkdir(exist_ok=True)
    
    search_queries = {
        'crack': [
            'surface crack concrete',
            'crack in material',
            'structural crack damage',
            'pavement crack',
            'concrete crack'
        ],
        'dent': [
            'metal dent damage',
            'car dent',
            'surface dent',
            'impact dent',
            'panel dent'
        ],
        'hole': [
            'hole in surface',
            'material hole damage',
            'corrosion hole',
            'surface hole',
            'puncture damage'
        ],
        'leak': [
            'water leak damage',
            'pipe leak',
            'roof leak',
            'structural leak',
            'leak damage'
        ]
    }
    
    total_downloaded = 0
    
    for defect_type, queries in search_queries.items():
        defect_dir = output_dir / defect_type
        defect_dir.mkdir(exist_ok=True)
        
        images_per_query = 50  # ~250 total per defect type
        
        for query in queries:
            print(f"\n📥 Downloading: {query}")
            
            try:
                downloader.download(
                    query=query,
                    limit=images_per_query,
                    output_dir='dataset',
                    adult_filter_off=True,
                    force_replace=False,
                    timeout=15,
                    verbose=False,
                    chromedriver=None  # Use system chrome
                )
                print(f"  ✓ Downloaded {images_per_query} images for: {query}")
                total_downloaded += images_per_query
                
            except Exception as e:
                print(f"  ⚠️  Error downloading {query}: {str(e)}")
                continue
    
    print(f"\n✅ Total downloaded: {total_downloaded} images")
    return True


if __name__ == '__main__':
    print("="*60)
    print("Alternative Web Scraper - Using bing-image-downloader")
    print("="*60)
    
    # Check if library is installed
    try:
        import bing_image_downloader
        print("✓ bing-image-downloader is installed")
        scrape_with_bing_downloader()
    except ImportError:
        print("\n❌ bing-image-downloader not installed")
        print("\nTo install, run:")
        print("  pip install bing-image-downloader")
        print("\nThen run this script again.")
