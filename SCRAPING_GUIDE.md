# 🌐 Web Scraping Setup Guide

## Overview
Download ~1000 defect images (cracks, dents, holes, leaks) for training data expansion.

---

## ⚡ Quick Start (Recommended)

### Option 1: Using bing-image-downloader (EASIEST)

**Step 1: Install required packages**
```powershell
pip install bing-image-downloader requests pillow
```

**Step 2: Run the scraper**
```powershell
python scrape_alternative.py
```

This will:
- Download ~250 images per defect type
- Organize them by category
- Create a log file with details
- Take ~30-45 minutes

---

## 📦 Installation Guide

### For Windows:

**1. Install dependencies**
```powershell
# Navigate to your project folder
cd "C:\Users\Ahmed\OneDrive\Desktop\Everything\Stage Wedtect"

# Install all required packages
pip install requests pillow bing-image-downloader opencv-python
```

**2. Verify installation**
```powershell
python -c "import requests; import PIL; import bing_image_downloader; print('✓ All packages installed')"
```

---

## 🚀 Running the Scrapers

### Method 1: bing-image-downloader (Recommended)
```powershell
python scrape_alternative.py
```

**Pros:**
- ✅ Most reliable
- ✅ Built-in error handling
- ✅ Automatic rate limiting
- ✅ Parallel downloads

**Cons:**
- Requires Selenium/ChromeDriver for best results
- Slightly slower than direct downloads

---

### Method 2: Direct URL Scraping
```powershell
python scrape_defect_images.py
```

**Pros:**
- ✅ Faster
- ✅ No browser needed
- ✅ Detailed logging

**Cons:**
- May need retries
- Some URLs might be blocked

---

## 📊 What You'll Get

After scraping completes, you'll have:

```
SCRAPED_IMAGES/
├── crack/
│   ├── crack_scraped_0001.jpg
│   ├── crack_scraped_0002.jpg
│   └── ... (~250 images)
├── dent/
│   ├── dent_scraped_0001.jpg
│   └── ... (~250 images)
├── hole/
│   └── ... (~250 images)
├── leak/
│   └── ... (~250 images)
└── scraping_log.txt
```

Total: **~1000 images**

---

## 🎯 Next Steps After Scraping

### 1. Review the Images
```powershell
# Open folder to review quality
explorer SCRAPED_IMAGES
```

### 2. Clean Up (Optional)
- Remove low-quality or irrelevant images
- Remove duplicates
- Keep ~900 best images

### 3. Annotate with Roboflow

**Free Option:**
- Upload to https://roboflow.com
- Use their annotation tools
- Export as YOLOv8 format
- Download labeled dataset

**Manual Option:**
- Use https://www.makesense.ai for free online annotation
- Or install: `pip install labelImg`

### 4. Merge with Training Data
```powershell
# Copy labeled images to your training folders
cp ROBOFLOW_OUTPUT/train/images/* TRAINING_DATA/train/images/
cp ROBOFLOW_OUTPUT/valid/images/* TRAINING_DATA/valid/images/
cp ROBOFLOW_OUTPUT/test/images/* TRAINING_DATA/test/images/

# Similarly for labels
cp ROBOFLOW_OUTPUT/train/labels/* TRAINING_DATA/train/labels/
# ... etc
```

### 5. Retrain Your Model
```powershell
python train_gpu.py
```

---

## ⚙️ Advanced Configuration

### Adjust Scraping Parameters

**In `scrape_defect_images.py`, modify:**

```python
DEFECT_TYPES = {
    'crack': 300,    # Images per defect type
    'dent': 300,
    'hole': 300,
    'leak': 300
}
```

### Custom Search Queries

**In `scrape_alternative.py`, modify:**

```python
search_queries = {
    'crack': [
        'your custom query 1',
        'your custom query 2',
        # ... add more
    ]
}
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
```
Solution: pip install --upgrade requests pillow bing-image-downloader
```

### Issue: Download rate too slow
```
Solution: Increase num_images per query in config
or use: pip install bing-image-downloader --upgrade
```

### Issue: Images are corrupted
```
Solution: Script automatically removes corrupted images
or run: python scrape_defect_images.py (has cleanup)
```

### Issue: Bing blocks the scraper
```
Solution: 
- Wait 5-10 minutes and retry
- Use VPN (optional)
- Try different search queries
```

---

## 📈 Expected Results

**Quality Metrics:**
- ✅ Valid image count: 90-95% of downloaded
- ✅ Average image size: 50-200 KB
- ✅ Formats: JPEG, PNG, WebP
- ✅ Relevant to defect types: 85-90%

**Typical Timeline:**
- Installation: 2-3 minutes
- Scraping: 30-45 minutes
- Cleanup: 5-10 minutes
- Annotation (Roboflow): 1-2 hours
- Retraining: 2-3 hours

---

## 💾 Saving Your Scraping Config

Create a `scraping_config.json` for future use:

```json
{
  "defect_types": {
    "crack": 250,
    "dent": 250,
    "hole": 250,
    "leak": 250
  },
  "output_dir": "SCRAPED_IMAGES",
  "timeout": 10,
  "retry_attempts": 3,
  "images_per_query": 50,
  "cleanup_corrupted": true
}
```

---

## 🔗 Useful Resources

1. **Roboflow** (annotation): https://roboflow.com
2. **makesense.ai** (online annotation): https://www.makesense.ai
3. **labelImg** (desktop tool): `pip install labelimg`
4. **bing-image-downloader**: https://github.com/bing-image-downloader/bing-image-downloader

---

## ❓ FAQ

**Q: Is web scraping legal?**
A: Yes, for personal/research purposes with proper attribution.

**Q: How many images do I need?**
A: 1000+ per class for best results. More = better generalization.

**Q: Will this violate copyright?**
A: These are for training only. Proper attribution is recommended.

**Q: Can I scrape other sources?**
A: Yes, modify the `search_queries` to target specific websites.

---

## 🎯 Tips for Success

1. ✅ Start with 1000 images and assess quality
2. ✅ Use diverse search queries for better variety
3. ✅ Clean up low-quality images before annotation
4. ✅ Annotate carefully (quality > quantity)
5. ✅ Merge with original training data gradually
6. ✅ Validate improvements with test set

---

**Ready to expand your dataset? 🚀**
Run: `pip install bing-image-downloader requests pillow && python scrape_alternative.py`
