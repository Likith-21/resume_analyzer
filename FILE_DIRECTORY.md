# 📂 PROJECT FILE DIRECTORY & DESCRIPTIONS

## Project Root: `d:\final\resume-screening-system\`

### Main Application Files

#### 1. **app.py** (600+ lines)
- **Purpose**: Main Streamlit web application
- **Functions**: 
  - main() - Application entry point
  - resume_screening_page() - Resume upload & analysis
  - job_recommendations_page() - Job matching results
  - skill_gap_analysis_page() - Skill gap analysis
  - about_page() - Information and help
  - load_jobs_data() - Load jobs from CSV
  - save_uploaded_file() - Handle file uploads
- **Run**: `streamlit run app.py`
- **Browser**: `http://localhost:8501`

#### 2. **config.py** (30 lines)
- **Purpose**: Project configuration and constants
- **Contains**:
  - Project name and version
  - File upload limits
  - Algorithm weights (60% similarity, 40% skills)
  - Top recommendations count
  - Skill categories list

#### 3. **test_demo.py** (250+ lines)
- **Purpose**: Test suite to verify all modules work
- **Tests**:
  - test_data_files() - Check skills and jobs loaded
  - test_resume_parser() - Email, phone, URL extraction
  - test_skill_extractor() - Skill detection
  - test_job_matcher() - Job matching algorithm
  - test_skill_gap() - Gap analysis
- **Run**: `D:\final\.venv\Scripts\python.exe test_demo.py`
- **Expected**: 5/5 tests passed ✅

---

### Python Modules (in `modules/` folder)

#### 1. **modules/resume_parser.py** (200+ lines)
- **Class**: ResumeParser
- **Methods**:
  - extract_text_from_pdf(file_path) - Parse PDF files
  - extract_text_from_docx(file_path) - Parse DOCX files
  - extract_text_from_file(file_path) - Auto-detect format
  - extract_email(text) - Find email addresses
  - extract_phone(text) - Find phone numbers
  - extract_urls(text) - Find LinkedIn, GitHub URLs
  - clean_text(text) - Clean and normalize text
- **Dependencies**: PyPDF2, docx, re (regex)

#### 2. **modules/skill_extractor.py** (200+ lines)
- **Class**: SkillExtractor
- **Methods**:
  - extract_skills(resume_text) → List[str] - Find all skills
  - extract_skills_by_category(resume_text) → Dict - Organized skills
  - extract_education(resume_text) → List[str] - Find degrees
  - estimate_experience_years(resume_text) → int - Years of experience
  - get_skill_score(detected_skills) → float - Score 0-100
- **Features**:
  - 122 technical skills database
  - 9 skill categories
  - NLP-based detection
  - Weighted scoring

#### 3. **modules/job_matcher.py** (200+ lines)
- **Class**: JobMatcher
- **Methods**:
  - prepare_job_descriptions() - Vectorize jobs
  - calculate_similarity(resume_text) → List - TF-IDF similarity
  - match_by_skills(resume_skills) → List - Skill matching
  - get_top_recommendations(resume_text, skills, top_n) → List - Top jobs
  - analyze_skill_gap(resume_skills, job_title) → Dict - Gap analysis
- **Algorithm**:
  - TF-IDF vectorization (scikit-learn)
  - Cosine similarity metrics
  - Combined scoring formula

---

### Data Files (in `data/` folder)

#### 1. **data/skills_database.py** (80 lines)
- **Content**: 122 technical skills organized in 9 categories
- **Categories**:
  - programming_languages (20+ skills)
  - web_technologies (15+ skills)
  - database (10+ skills)
  - machine_learning (20+ skills)
  - data_science (10+ skills)
  - cloud_platforms (10+ skills)
  - big_data (10+ skills)
  - devops (10+ skills)
  - soft_skills (10+ skills)
- **Functions**:
  - get_all_skills() - Returns flat list of all skills
  - get_skills_by_category(category) - Returns skills by category

#### 2. **data/jobs.csv** (18 rows)
- **Format**: CSV with headers
- **Columns**:
  - job_id (1-15)
  - job_title (Data Scientist, ML Engineer, etc.)
  - company (TechCorp, AI Solutions, etc.)
  - job_description (Detailed job description text)
  - required_skills (Comma-separated list)
  - experience_years (Required years)
  - location (City name)
  - salary_range (e.g., 120000-160000)
- **Sample Jobs**:
  1. Data Scientist - TechCorp
  2. Machine Learning Engineer - AI Solutions
  3. Data Analyst - Finance Plus
  4. Full Stack Developer - WebDev Inc
  5. Backend Engineer - CloudTech
  (15 total jobs)

---

### Documentation Files

#### 1. **README.md** (500+ lines)
- **Content**:
  - Project overview and features
  - Technology stack description
  - Installation instructions
  - User guide and examples
  - Matching algorithm explanation
  - Viva Q&A sample questions
  - Future enhancement ideas

#### 2. **SETUP_GUIDE.md** (400+ lines)
- **Content**:
  - Quick start (5 minutes)
  - Complete installation steps
  - Module descriptions
  - How to run the application
  - Testing instructions
  - Troubleshooting guide
  - Performance metrics
  - Deployment options (Streamlit Cloud, Heroku, Docker)

#### 3. **QUICK_START.md** (200+ lines)
- **Content**:
  - 3-step quick startup
  - What you can do immediately
  - File structure overview
  - Environment status
  - Browser access
  - Common issues and fixes
  - Next steps

#### 4. **PROJECT_SUMMARY.md** (This file category)
- **Content**:
  - Project completion summary
  - What has been done
  - Features implemented
  - How to run
  - For viva presentation
  - Final checklist

#### 5. **FILE_DIRECTORY.md** (This file)
- **Content**:
  - Complete file listing
  - File purposes
  - How to use each file
  - Quick reference

---

### Configuration & Project Files

#### 1. **requirements.txt** (11 lines)
- Lists all Python package dependencies
- Versions pinned for reproducibility
- Packages:
  - streamlit (UI)
  - pandas (data processing)
  - numpy (numerical)
  - scikit-learn (ML)
  - PyPDF2 (PDF parsing)
  - python-docx (DOCX parsing)
  - spacy (NLP)
  - nltk (NLP)
  - matplotlib, seaborn (visualization)
  - pillow (images)

#### 2. **.gitignore**
- Specifies which files to exclude from version control
- Ignores: __pycache__, .venv, uploads/, build/, dist/, .DS_Store, etc.
- Standard Python project ignores

#### 3. **SAMPLE_RESUME.txt**
- Sample resume text for testing
- Includes:
  - Name: John Smith
  - Contact info
  - Technical skills
  - Work experience
  - Education
  - Certifications
  - Projects
- Use for testing when you don't have real resume

---

### Package Initialization Files

#### 1. **modules/__init__.py**
- Makes modules folder a Python package
- Allows importing from modules folder

#### 2. **data/__init__.py**
- Makes data folder a Python package
- Allows importing from data folder

---

### Folders

#### 1. **.venv/** (Virtual Environment)
- Python virtual environment (3.11.9)
- Contains installed packages
- Isolated from system Python
- Already configured ✅

#### 2. **uploads/** (User Uploaded Files)
- Stores user-uploaded resume files
- Creates .gitkeep by default
- Files automatically cleaned if needed

#### 3. **data/** (Data Files)
- Contains skills database and jobs CSV
- Can be expanded with more jobs/skills

#### 4. **modules/** (Python Modules)
- Contains all custom modules
- Separated for modularity and reusability

---

## 📊 File Statistics

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| Application | 1 | 600+ | Main web app |
| Modules | 3 | 600+ | Core functionality |
| Configuration | 1 | 30 | Settings |
| Data Storage | 2 | 100+ | Skills & Jobs |
| Testing | 1 | 250+ | Verification |
| Documentation | 5 | 1500+ | Guides |
| **Total** | **13** | **3000+** | **Full system** |

---

## 🔍 File Dependencies

```
app.py
├── modules/resume_parser.py
├── modules/skill_extractor.py
│   └── data/skills_database.py
├── modules/job_matcher.py
│   └── data/jobs.csv
├── config.py
└── Built-in libraries (streamlit, pandas, sklearn, etc.)

test_demo.py
├── modules/resume_parser.py
├── modules/skill_extractor.py
│   └── data/skills_database.py
├── modules/job_matcher.py
│   └── data/jobs.csv
└── Built-in libraries
```

---

## 🚀 How to Use This Directory

### 1. Run the Application
```bash
# Start the web application
streamlit run app.py
```

### 2. Run Tests
```bash
# Test all modules
D:\final\.venv\Scripts\python.exe test_demo.py
```

### 3. Add Custom Data
```bash
# Add more jobs to data/jobs.csv
# Add more skills to data/skills_database.py
# Restart app to see changes
```

### 4. Modify UI
```bash
# Edit app.py CSS section
# Modify colors, layout, styling
# Restart app to see changes
```

### 5. Update Logic
```bash
# Modify algorithms in modules/job_matcher.py
# Change weights in config.py
# Restart app to apply changes
```

---

## 📋 Quick File Reference

### To Find...
- **Resume parsing code** → `modules/resume_parser.py`
- **Skill detection** → `modules/skill_extractor.py`
- **Job matching** → `modules/job_matcher.py`
- **Skills database** → `data/skills_database.py`
- **Job data** → `data/jobs.csv`
- **Web interface** → `app.py`
- **Setup help** → `SETUP_GUIDE.md`
- **Quick start** → `QUICK_START.md`
- **Full docs** → `README.md`
- **Tests** → `test_demo.py`

---

## ✅ All Files Present

- ✅ 3 Python modules (700+ lines)
- ✅ 1 Main application (600+ lines)
- ✅ 1 Test suite (250+ lines)
- ✅ 5 Documentation files (1500+ lines)
- ✅ 2 Data files (122 skills, 15 jobs)
- ✅ 1 Config file
- ✅ 1 .gitignore
- ✅ 1 requirements.txt
- ✅ 2 Package init files
- ✅ 3 Folders (modules, data, uploads)

**Total: 13 files, 3000+ lines, ready to use!**

---

## 🎯 Next Steps

1. Read QUICK_START.md (2 minutes)
2. Run the app: `streamlit run app.py` (1 minute)
3. Test with sample resume (5 minutes)
4. Explore all features (10 minutes)
5. Customize as needed (Variable)

---

**You have everything you need to build and present an impressive AI & DS project!**
