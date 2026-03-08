# AI Resume Screening & Job Recommendation System

A comprehensive AI-powered system that analyzes resumes and recommends suitable jobs using Natural Language Processing and Machine Learning.

## 🎯 Project Overview

This system helps job seekers find the most suitable positions based on their skills, experience, and qualifications. It uses advanced NLP techniques to extract information from resumes and matches them with job descriptions using similarity algorithms.

## ✨ Key Features

### 1. **Resume Screening & Analysis**
- Upload resumes in PDF/DOCX format
- Extract text automatically
- Detect contact information (email, phone, URLs)
- Identify educational qualifications
- Estimate years of experience
- Generate skill score

### 2. **Skill Extraction**
- Identify 100+ technical skills
- Categorize skills by domain:
  - Programming Languages
  - Web Technologies
  - Database Technologies
  - Machine Learning & AI
  - Data Science
  - Cloud Platforms
  - DevOps & Infrastructure
  - Big Data Technologies
  - Soft Skills

### 3. **Job Matching Algorithm**
- TF-IDF vectorization for content matching
- Cosine similarity for resume-job matching
- Combined scoring system:
  - 60% Content similarity
  - 40% Skills matching
- Rank jobs by relevance

### 4. **Job Recommendations**
- Get top 10 job recommendations
- View detailed match breakdown
- Identify matching and missing skills
- Check location and salary information
- See experience requirements

### 5. **Skill Gap Analysis**
- Analyze specific job requirements
- Find missing skills for target positions
- Identify experience gaps
- Get actionable learning recommendations

## 🛠️ Technology Stack

```
Programming Language: Python 3.8+
Frontend: Streamlit
Data Processing: Pandas, NumPy
Machine Learning: Scikit-learn
NLP: SpaCy, NLTK
Resume Parsing: PyPDF2, python-docx
Text Vectorization: TF-IDF
```

## 📁 Project Structure

```
resume-screening-system/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
│
├── modules/
│   ├── resume_parser.py           # PDF/DOCX text extraction
│   ├── skill_extractor.py         # NLP-based skill extraction
│   └── job_matcher.py             # Job matching algorithm
│
├── data/
│   ├── skills_database.py         # Technical skills database
│   └── jobs.csv                   # Job descriptions dataset
│
├── uploads/                        # Uploaded resume files
└── README.md                       # Project documentation
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Clone the Repository
```bash
cd d:\final\resume-screening-system
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Models (Optional)
```bash
python -m spacy download en_core_web_sm
```

## 💻 Running the Application

### Option 1: Run with Streamlit
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Option 2: Run from Command Line
```bash
streamlit run d:\final\resume-screening-system\app.py
```

## 📖 User Guide

### Step 1: Upload Resume
1. Go to **"Resume Screening"** tab
2. Upload your resume (PDF or DOCX)
3. System automatically extracts information

### Step 2: View Analysis
- See detected skills organized by category
- Check extracted contact information
- Review estimated experience
- View overall skill score

### Step 3: Get Job Recommendations
1. Navigate to **"Job Recommendations"** tab
2. View top 10 matching jobs
3. Check match percentage breakdown:
   - Skill match percentage
   - Content similarity score
   - Matching and missing skills

### Step 4: Analyze Skill Gaps
1. Go to **"Skill Gap Analysis"** tab
2. Select a target job
3. See:
   - Skills you have (matching)
   - Skills you need to learn (missing)
   - Experience gap analysis
   - Learning recommendations

## 🧪 Example Usage

### Sample Resume Skills Detected:
```
Programming: Python, Java, SQL
Machine Learning: TensorFlow, PyTorch, Scikit-learn
Data Science: Pandas, NumPy, Matplotlib
Cloud: AWS, Docker, Kubernetes
```

### Sample Job Recommendations:
```
1. Data Scientist at TechCorp - 88% Match
   ✅ Matching: Python, ML, SQL
   ❌ Missing: TensorFlow, AWS

2. ML Engineer at AI Solutions - 83% Match
   ✅ Matching: Deep Learning, PyTorch
   ❌ Missing: NLP, Kubernetes
```

## 📊 Matching Algorithm

### TF-IDF Similarity
- Vectorizes resume and job descriptions
- Calculates cosine similarity
- Ranges from 0-100%

### Skill Matching
- Matches extracted skills with job requirements
- Calculates skill match percentage
- Weighted by skill importance

### Combined Score
```
Final Score = (TF-IDF Score × 0.6) + (Skill Match × 0.4)
```

## 🎓 Viva Questions & Answers

### Q1: What is NLP?
**A:** Natural Language Processing is a field of AI that helps computers understand and process human language. We use it to extract skills and information from resumes.

### Q2: What is TF-IDF?
**A:** TF-IDF (Term Frequency-Inverse Document Frequency) is a vectorization technique that converts text into numerical values based on word importance.

### Q3: How does resume matching work?
**A:** We convert resume and job descriptions into vectors, then calculate similarity using cosine similarity metric (0-1 scale, converted to percentage).

### Q4: What is Cosine Similarity?
**A:** It measures the angle between two vectors. A value of 1 means identical documents, 0 means completely different.

### Q5: How are skills extracted?
**A:** Using keyword matching against a database of 100+ technical skills, combined with NLP techniques for context understanding.

### Q6: How is the score calculated?
**A:** 60% from document similarity (TF-IDF) + 40% from skill matching percentage.

### Q7: What dataset is used?
**A:** A custom dataset of 15 jobs from Kaggle and real job postings with various title, skills, and requirements.

### Q8: How to improve matching accuracy?
**A:** By using more training data, fine-tuning weights, implementing BERT-based embeddings, or using deep learning models.

## 🌟 Impressive Features for Viva

✅ **Full NLP Pipeline** - From text extraction to analysis

✅ **Multiple ML Algorithms** - TF-IDF, Cosine Similarity, Skill Matching

✅ **Real-World Application** - HR automation, job recommendations

✅ **User-Friendly Interface** - Interactive Streamlit web app

✅ **Comprehensive Analysis** - Skills, education, experience, gaps

✅ **Scalable Design** - Can handle large resume/job datasets

✅ **Production-Ready Code** - Proper error handling, modular design

## 🚀 Future Enhancements

1. **BERT-based Embeddings** - Replace TF-IDF with transformer models
2. **Deep Learning Models** - Implement neural networks for better matching
3. **LinkedIn Integration** - Import profile data directly
4. **Resume Scoring** - ML-based resume quality scoring
5. **Company Insights** - Glassdoor ratings, company info
6. **Interview Prep** - Questions based on job requirements
7. **Skill Courses** - Recommend online courses for missing skills
8. **Database Integration** - Store user profiles and preferences

## 📝 Sample Output

### Resume Analysis:
```
Total Skills Detected: 12
Estimated Experience: 4 years
Skill Score: 78.5/100
Education: B.Tech, M.Tech
```

### Job Recommendations:
```
1. Data Scientist - 87% Match
   Matching Skills: Python, ML, SQL, Data Analysis
   Missing Skills: TensorFlow, AWS

2. ML Engineer - 82% Match
   Matching Skills: Python, Deep Learning, PyTorch
   Missing Skills: NLP, Kubernetes
```

## 🤝 Contributing

Feel free to fork this project and contribute improvements!

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author Notes

This project is designed as a comprehensive final year AI & Data Science project that demonstrates:
- Machine Learning application
- Natural Language Processing
- Data Analysis
- Full-stack Python development
- Real-world problem solving

Perfect for placements and viva presentations!

---

**Built with ❤️ using Python, Streamlit, and Machine Learning**
