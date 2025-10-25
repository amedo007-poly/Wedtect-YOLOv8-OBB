# 🌐 Web Scraping - Ready to Start!

## ✅ Setup Complete

All dependencies are installed and ready:
- ✓ `bing-image-downloader` - Download images from Bing
- ✓ `requests` - Handle HTTP requests
- ✓ `pillow` - Image processing
- ✓ `urllib` - URL handling

---

## 🚀 Quick Start (Choose One)

### **Option 1: Easy & Recommended** (bing-image-downloader)
```powershell
python scrape_alternative.py
```
**What it does:**
- Downloads ~250 images per defect type (crack, dent, hole, leak)
- Total: ~1000 images
- Time: 30-45 minutes
- Auto-organizes by category

### **Option 2: Advanced** (Direct URL scraping)
```powershell
python scrape_defect_images.py
```
**What it does:**
- Same as Option 1 but with detailed logging
- Better control and error handling
- More customizable

---

## 📊 What You'll Get

```
SCRAPED_IMAGES/
├── crack/          (~250 images)
├── dent/           (~250 images)
├── hole/           (~250 images)
├── leak/           (~250 images)
├── scraping_log.txt
└── ORGANIZED_SCRAPED_DATA/  (for organization)
```

---

## ⏱️ Timeline

| Step | Time | Action |
|------|------|--------|
| 1 | 2 min | Run scraper command |
| 2 | 30-45 min | Scraper downloads images |
| 3 | 5 min | Review downloaded images |
| 4 | 1-2 hrs | Upload to Roboflow & annotate |
| 5 | 2-3 hrs | Retrain model with new data |

---

## 🎯 After Scraping: Next Steps

### Step 1: Review Images (Quality Check)
```powershell
# Open the downloaded images folder
explorer SCRAPED_IMAGES
```
- ✓ Check image quality
- ✓ Remove irrelevant/corrupted images
- ✓ Keep best ~900 images

### Step 2: Annotate with Roboflow

**Free Account at:** https://roboflow.com

```
1. Go to Roboflow.com
2. Create free account
3. Create new project
4. Upload your SCRAPED_IMAGES folder
5. Use Roboflow's AI auto-labeling feature
6. Refine labels manually
7. Export as YOLOv8 format
8. Download the labeled dataset
```

### Step 3: Merge with Your Training Data
```powershell
# Copy the labeled images to your training folders
# Make sure directory structure matches:

# Copy images
Copy-Item "Roboflow_output/train/images/*" -Destination "TRAINING_DATA/train/images/"
Copy-Item "Roboflow_output/valid/images/*" -Destination "TRAINING_DATA/valid/images/"
Copy-Item "Roboflow_output/test/images/*" -Destination "TRAINING_DATA/test/images/"

# Copy labels
Copy-Item "Roboflow_output/train/labels/*" -Destination "TRAINING_DATA/train/labels/"
Copy-Item "Roboflow_output/valid/labels/*" -Destination "TRAINING_DATA/valid/labels/"
Copy-Item "Roboflow_output/test/labels/*" -Destination "TRAINING_DATA/test/labels/"

# Update data.yaml to reflect new counts
```

### Step 4: Retrain Your Model
```powershell
python train_gpu.py
```

Your model will automatically:
- Load the expanded dataset
- Retrain with all data (original + scraped + annotated)
- Generate improved performance metrics
- Save the better model to DEPLOYMENT/model/best.pt

---

## 💡 Pro Tips

1. **Start Scraping:**
   - Be patient - first run takes 30-45 minutes
   - Don't close the terminal while running
   - Check internet connection stability

2. **Quality Over Quantity:**
   - Remove blurry/irrelevant images
   - Keep diverse examples
   - Prioritize high-quality defect images

3. **Roboflow Tips:**
   - Use AI auto-labeling (saves time)
   - Manually verify important labels
   - Keep consistent class definitions
   - Export only high-confidence annotations

4. **Retraining:**
   - Start with 50% old + 50% new data
   - Monitor performance metrics
   - Gradually increase new data percentage

---

## 🔍 Monitoring Scraping Progress

While the scraper runs, you'll see:
```
📥 Downloading: surface crack concrete
  ✓ Downloaded 50 images for: surface crack concrete
  
📥 Downloading: crack in material
  ✓ Downloaded 50 images for: crack in material
  
... (continues for all searches) ...

✅ Total downloaded: 1000 images
```

A log file is created: `SCRAPED_IMAGES/scraping_log.txt`

---

## 🛠️ Troubleshooting

### Scraper runs but downloads are slow
- This is normal - respect Bing's rate limiting
- First batch: ~50 images per query = 5-10 min per defect type
- Total: 30-45 minutes expected

### Some images fail to download
- Normal - some URLs may be invalid
- Script automatically handles failures
- Still collects 80-95% of target images

### Want to customize searches?
Edit `scrape_alternative.py` or `scrape_defect_images.py`:
```python
search_queries = {
    'crack': [
        'your custom query 1',
        'your custom query 2',
    ],
    # ... etc
}
```

---

## 📚 Full Documentation

See: `SCRAPING_GUIDE.md` for:
- ✓ Detailed installation instructions
- ✓ Advanced configuration options
- ✓ Troubleshooting FAQ
- ✓ Recommended tools and resources
- ✓ Best practices

---

## 🎬 Ready?

**Run this command to start scraping:**

```powershell
python scrape_alternative.py
```

**Or use the advanced version:**

```powershell
python scrape_defect_images.py
```

**Then follow the "After Scraping: Next Steps" above.**

---

**Good luck! 🚀 Your dataset expansion starts now!**
