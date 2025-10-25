"""
Web Scraper - Working Version with Multiple Methods
===================================================
Uses Bing Image Search API + manual download capability
"""

import os
import requests
from pathlib import Path
from urllib.parse import quote
import time
import json

def scrape_bing_direct():
    """
    Scrape images directly from Bing Image Search
    No browser required, simple and reliable
    """
    
    output_dir = Path('SCRAPED_IMAGES')
    output_dir.mkdir(exist_ok=True)
    
    defect_types = {
        'crack': ['concrete crack', 'surface crack', 'structural crack', 'pavement crack', 'material crack'],
        'dent': ['metal dent', 'car dent', 'surface dent', 'impact damage', 'dent damage'],
        'hole': ['hole damage', 'corrosion hole', 'material hole', 'puncture hole', 'structural hole'],
        'leak': ['water leak', 'pipe leak', 'roof leak', 'damage leak', 'moisture leak']
    }
    
    total_downloaded = 0
    
    for defect_type, searches in defect_types.items():
        defect_dir = output_dir / defect_type
        defect_dir.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"📥 Downloading {defect_type.upper()} images...")
        print(f"{'='*60}")
        
        downloaded_for_type = 0
        
        for search_query in searches:
            print(f"\n🔍 Searching: {search_query}")
            
            try:
                # Bing Image Search URL (works without browser)
                search_url = f"https://www.bing.com/images/search?q={quote(search_query)}"
                
                # Alternative: Use direct image URLs
                # This fetches image URLs from Bing without JavaScript
                urls = scrape_bing_urls(search_query, num_images=50)
                
                if not urls:
                    print(f"  ⚠️  No URLs found for: {search_query}")
                    continue
                
                print(f"  Found {len(urls)} image URLs")
                
                # Download each image
                for idx, url in enumerate(urls, 1):
                    try:
                        filename = f"{defect_type}_{len(os.listdir(defect_dir)) + 1}.jpg"
                        filepath = defect_dir / filename
                        
                        # Skip if already exists
                        if filepath.exists():
                            continue
                        
                        # Download image
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        response = requests.get(url, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            # Verify it's a valid image
                            if filepath.stat().st_size > 5000:  # At least 5KB
                                print(f"  ✓ Downloaded: {filename} ({response.stat().st_size // 1024}KB)")
                                downloaded_for_type += 1
                                total_downloaded += 1
                            else:
                                filepath.unlink()  # Delete if too small
                        
                    except Exception as e:
                        continue
                    
                    # Rate limiting
                    time.sleep(0.2)
                
                # Stop if we have enough for this search
                if downloaded_for_type >= 250:
                    break
                    
            except Exception as e:
                print(f"  ❌ Error with {search_query}: {str(e)}")
                continue
        
        print(f"\n✅ Downloaded {downloaded_for_type} images for {defect_type}")
    
    print(f"\n\n{'='*60}")
    print(f"🎉 COMPLETE: Total {total_downloaded} images downloaded")
    print(f"{'='*60}")
    return total_downloaded > 0


def scrape_bing_urls(query, num_images=50):
    """
    Extract image URLs from Bing Image Search
    Returns list of direct image URLs
    """
    urls = []
    
    try:
        # Bing Image Search URL
        search_url = f"https://cn.bing.com/images/search?q={quote(query)}&first=1&count={num_images}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return []
        
        # Extract image URLs using regex (simple but effective)
        import re
        
        # Find image URLs in HTML
        pattern = r'murl":"([^"]+)"'
        matches = re.findall(pattern, response.text)
        
        for match in matches[:num_images]:
            if match and 'http' in match:
                # Unescape URL
                url = match.replace('\\/', '/')
                urls.append(url)
        
    except Exception as e:
        print(f"  Error scraping URLs: {str(e)}")
    
    return urls


def manual_download_guide():
    """
    If automated fails, provide manual download instructions
    """
    print("""
    
╔════════════════════════════════════════════════════════════╗
║          MANUAL DOWNLOAD GUIDE                             ║
╚════════════════════════════════════════════════════════════╝

If automated scraping doesn't work, follow these steps:

1. Go to: https://www.bing.com/images
2. Search for each defect type:
   - "concrete crack damage"
   - "metal dent damage"
   - "surface hole damage"
   - "water leak damage"

3. Download images (~250 per type)
4. Save to: SCRAPED_IMAGES/{defect_type}/
   
   Example:
   SCRAPED_IMAGES/
   ├── crack/ (250 images here)
   ├── dent/  (250 images here)
   ├── hole/  (250 images here)
   └── leak/  (250 images here)

5. Or use this tool: https://github.com/Buddybenj/Bing-Image-Downloader
   
   pip install bing-image-downloader
   
   from bing_image_downloader import downloader
   downloader.download(
       query="concrete crack",
       limit=250,
       output_dir="SCRAPED_IMAGES/crack",
       adult_filter_off=True,
       force_replace=False,
       chromedriver=None
   )

═══════════════════════════════════════════════════════════════
    """)


if __name__ == '__main__':
    print("="*60)
    print("🌐 Web Image Scraper - Bing Direct Method")
    print("="*60)
    print("\nStarting image download...")
    print("(This may take 5-10 minutes)\n")
    
    try:
        success = scrape_bing_direct()
        
        if not success:
            print("\n⚠️  Automated scraping had issues.")
            manual_download_guide()
        else:
            print("\n✅ Scraping completed successfully!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        manual_download_guide()
