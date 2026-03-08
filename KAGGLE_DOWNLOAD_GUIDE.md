# 📚 KAGGLE DATASET DOWNLOAD GUIDE

## Step-by-Step Instructions to Download Datasets

### 1️⃣ CREATE KAGGLE ACCOUNT & API KEY

#### Step 1: Create Kaggle Account
1. Go to: https://www.kaggle.com
2. Click "Sign Up"
3. Create account with email and password
4. Verify your email

#### Step 2: Generate API Key
1. Go to: https://www.kaggle.com/settings/account
2. Click "Create New API Token"
3. A file `kaggle.json` will download
4. Save it in your user home directory:
   - **Windows:** `C:\Users\YourUsername\.kaggle\kaggle.json`
   - **Mac/Linux:** `~/.kaggle/kaggle.json`

#### Step 3: Install Kaggle CLI
```bash
pip install kaggle
```

Verify installation:
```bash
kaggle datasets list
```

---

## 2️⃣ RECOMMENDED KAGGLE DATASETS TO DOWNLOAD

### Dataset 1: Updated Resume Dataset (Recommended)
**Name:** Updated Resume Dataset  
**URL:** https://www.kaggle.com/datasets/udacity/resume-data  
**Records:** 1000+ resumes  
**Size:** ~50 MB

**Download Command:**
```bash
kaggle datasets download -d udacity/resume-data
```

**What it contains:**
- Resume text
- Resume category (class)
- Structured resume data

**Use for:** Training resume category classifier

---

### Dataset 2: Resume Dataset for NLP
**Name:** Resume Dataset  
**URL:** https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset  
**Records:** 2000+ resumes  
**Size:** ~30 MB

**Download Command:**
```bash
kaggle datasets download -d snehaanbhawal/resume-dataset
```

**What it contains:**
- Resume ID and text
- Job category labels
- Structured data

**Use for:** NLP model training, skill extraction

---

### Dataset 3: Job Descriptions Dataset
**Name:** Job Description Dataset  
**URL:** https://www.kaggle.com/datasets/nikitagrgupta/job-descriptions  
**Records:** 5000+ job postings  
**Size:** ~10 MB

**Download Command:**
```bash
kaggle datasets download -d nikitagrgupta/job-descriptions
```

**What it contains:**
- Job title
- Job description
- Company
- Location
- Salary data

**Use for:** Enhance job database, train better matching

---

### Dataset 4: Data Science Job Salary Dataset
**Name:** Data Science Job Salary Dataset  
**URL:** https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries  
**Records:** 600+ job records  
**Size:** ~100 KB

**Download Command:**
```bash
kaggle datasets download -d ruchi798/data-science-job-salaries
```

**What it contains:**
- Job title
- Salary
- Company
- Experience level
- Skills required

**Use for:** Salary prediction, experience-based recommendations

---

## 3️⃣ HOW TO DOWNLOAD ALL AT ONCE

Create a file `download_datasets.sh` (Mac/Linux) or `download_datasets.bat` (Windows):

### Windows Batch File
```batch
@echo off
echo Downloading Kaggle Datasets...

echo Downloading Updated Resume Dataset...
kaggle datasets download -d udacity/resume-data

echo Downloading Resume Dataset for NLP...
kaggle datasets download -d snehaanbhawal/resume-dataset

echo Downloading Job Descriptions Dataset...
kaggle datasets download -d nikitagrgupta/job-descriptions

echo Downloading Data Science Salary Dataset...
kaggle datasets download -d ruchi798/data-science-job-salaries

echo All datasets downloaded! Extracting...
for %%f in (*.zip) do (
    powershell -Command "Expand-Archive -Path '%%f' -DestinationPath 'datasets' -Force"
    del %%f
)

echo Done! Check 'datasets' folder.
```

### Mac/Linux Bash Script
```bash
#!/bin/bash
echo "Downloading Kaggle Datasets..."

mkdir -p datasets
cd datasets

echo "Downloading Updated Resume Dataset..."
kaggle datasets download -d udacity/resume-data

echo "Downloading Resume Dataset for NLP..."
kaggle datasets download -d snehaanbhawal/resume-dataset

echo "Downloading Job Descriptions Dataset..."
kaggle datasets download -d nikitagrgupta/job-descriptions

echo "Downloading Data Science Salary Dataset..."
kaggle datasets download -d ruchi798/data-science-job-salaries

echo "Extracting all files..."
unzip -q '*.zip'
rm *.zip

echo "Done! Check datasets folder."
```

---

## 4️⃣ ORGANIZE DOWNLOADED DATA

After downloading, create this folder structure:

```
d:\final\resume-screening-system\
├── data/
│   ├── existing_data/          (20 jobs, 260 skills)
│   │   ├── jobs.csv
│   │   ├── skills_database.py
│   │   └── resume_dataset.csv
│   │
│   └── kaggle_datasets/        (NEW - Kaggle data)
│       ├── resume-data/        (From udacity dataset)
│       │   ├── Resume.csv
│       │   ├── Resumes.csv
│       │   └── resume_data.csv
│       │
│       ├── resume-dataset/     (From snehaanbhawal dataset)
│       │   ├── Resume_data.csv
│       │   └── ResumesData.csv
│       │
│       ├── job-descriptions/   (From nikitagrgupta dataset)
│       │   ├── job_descriptions.csv
│       │   └── jobs.csv
│       │
│       └── salary-data/        (From ruchi798 dataset)
│           ├── salaries.csv
│           └── job_salaries.csv
```

---

## 5️⃣ MANUAL UPLOAD ALTERNATIVE

If you can't use Kaggle API:

1. **Download on Kaggle Website:**
   - Visit dataset page
   - Click "Download" button
   - Save ZIP file

2. **Extract Files:**
   - Right-click → Extract All
   - Move to `data/kaggle_datasets/` folder

3. **Rename for Consistency:**
   - Standardize filenames
   - Keep original column names
   - Add README with dataset mapping

---

## 6️⃣ VERIFY YOUR DOWNLOADS

After downloading, verify the data:

```python
import pandas as pd
import os

# Check resume data
resume_file = 'data/kaggle_datasets/resume-data/Resume.csv'
if os.path.exists(resume_file):
    df = pd.read_csv(resume_file)
    print(f"✅ Resume data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"   Columns: {df.columns.tolist()}")
else:
    print(f"❌ File not found: {resume_file}")

# Check job data
job_file = 'data/kaggle_datasets/job-descriptions/job_descriptions.csv'
if os.path.exists(job_file):
    df = pd.read_csv(job_file)
    print(f"✅ Job data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"   Columns: {df.columns.tolist()}")
else:
    print(f"❌ File not found: {job_file}")
```

---

## 7️⃣ EXPECTED FILE STRUCTURE AFTER DOWNLOAD

| Dataset | File | Records | Key Columns |
|---------|------|---------|-------------|
| Resume (Udacity) | Resume.csv | 1000+ | ID, Resume_str, Category |
| Resume (NLP) | ResumesData.csv | 2000+ | ID, Resume, Category |
| Jobs | job_descriptions.csv | 5000+ | job_title, description, company |
| Salary | salaries.csv | 600+ | job_title, salary, experience |

---

## 8️⃣ TROUBLESHOOTING

### Issue: "kaggle" command not found
```bash
# Solution: Install kaggle
pip install --upgrade kaggle

# Verify
kaggle --version
```

### Issue: "Authentication failed"
1. Check if `kaggle.json` is in `.kaggle` folder
2. Verify file permissions: `chmod 600 ~/.kaggle/kaggle.json`
3. Regenerate API token on Kaggle website

### Issue: "Dataset not found"
- Verify dataset URL is correct
- Check dataset is not restricted
- Try downloading from web browser instead

### Issue: File extraction fails
- Download latest 7-Zip or WinRAR
- Try: `unzip` command on Windows PowerShell
- Or: Extract manually using Windows Explorer

---

## ✅ NEXT STEPS

After downloading all datasets:

1. **Organize files** in `data/kaggle_datasets/`
2. **Run verification script** to check data
3. **Provide dataset locations** to me
4. **I will train models** on the data

---

## 📝 WHAT TO PROVIDE ME

Once you've downloaded and organized the data, provide:

```
Dataset sources you downloaded:
1. Resume Udacity Dataset - Located at: ___________
2. Resume NLP Dataset - Located at: ___________
3. Job Descriptions Dataset - Located at: ___________
4. Salary Dataset - Located at: ___________

File names in each folder:
- Resume files: ___________
- Job files: ___________
- Salary files: ___________

Column names (from first row of CSV):
Resume CSV columns: ___________
Job CSV columns: ___________
```

Then I'll:
1. Load and preprocess all data
2. Merge with existing datasets
3. Train skill classifier
4. Train category predictor
5. Evaluate models
6. Save trained models
7. Integrate into the system

---

**Ready to download? Let's build an even more powerful ML system!** 🚀
