# ML Model Training & Integration Guide

## Overview

This guide explains how to train ML models on your Kaggle datasets and integrate them with the resume screening system.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│          COMPLETE ML WORKFLOW                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Data Preprocessing (data_preprocessing.py)         │
│     ├─ Load Kaggle datasets                           │
│     ├─ Standardize columns                            │
│     ├─ Extract skills                                 │
│     └─ Create training dataset                        │
│                     ↓                                  │
│  2. Model Training (train_models.py)                   │
│     ├─ Train Resume Category Classifier               │
│     │  ├─ Logistic Regression                         │
│     │  ├─ Random Forest                               │
│     │  └─ Gradient Boosting                           │
│     ├─ Train Skill Extraction Models                  │
│     │  └─ Binary classifiers for top skills           │
│     └─ Evaluate & Save Models                         │
│                     ↓                                  │
│  3. Model Integration (model_integration.py)          │
│     ├─ Load trained models                            │
│     ├─ Make predictions                               │
│     └─ Enhance recommendations                        │
│                     ↓                                  │
│  4. Web Application (app.py)                          │
│     └─ Use trained models for better accuracy         │
│                                                       │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Prepare Kaggle Datasets

Refer to [KAGGLE_DOWNLOAD_GUIDE.md](KAGGLE_DOWNLOAD_GUIDE.md) for detailed instructions.

```bash
# Create Kaggle datasets directory
mkdir -p data/kaggle_datasets

# Download datasets (requires Kaggle API)
kaggle datasets download -d jillanisoftball/resume-data
kaggle datasets download -d snehaanbhawal/resume-nlp
kaggle datasets download -d kashnitsky/job-salary-data

# Extract to data/kaggle_datasets/
```

### 2. Run Complete Workflow

```bash
# This runs all steps automatically:
python complete_workflow.py
```

This will:
1. Setup directories
2. Load Kaggle data
3. Preprocess and clean data
4. Create training dataset
5. Train ML models
6. Generate training report

### 3. Verify Results

```bash
# Check training report
cat models/training_report.txt

# List trained models
ls -la models/
```

### 4. Run Web Application

```bash
streamlit run app.py
```

The web app will automatically use trained models if available.

## Detailed Component Guide

### Data Preprocessing (`data_preprocessing.py`)

**Purpose**: Convert raw Kaggle data into training-ready format

**Key Methods**:

```python
from data.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()

# Load from different Kaggle sources
udacity_df = preprocessor.load_resume_data_udacity('path/to/ResumesDataset.csv')
nlp_df = preprocessor.load_resume_data_nlp('path/to/Resume.csv')
jobs_df = preprocessor.load_job_data('path/to/jobs.csv')

# Standardize column names for consistency
clean_resumes = preprocessor.standardize_resume_columns(udacity_df)

# Extract technical skills using skill database
resumes_with_skills = clean_resumes.copy()
resumes_with_skills['extracted_skills'] = resumes_with_skills['resume_text'].apply(
    preprocessor.extract_skills_from_resume
)

# Create labeled training dataset
training_data = preprocessor.create_training_dataset(clean_resumes)

# Get dataset statistics
stats = preprocessor.get_dataset_statistics(training_data)
```

**Input CSV Formats Supported**:

Udacity Dataset:
- `ID`, `resume`, `category` (or similar)
- Columns: resume_text, label/category

NLP Dataset:
- `Resume`, `Category` (or similar)
- Columns: resume, category/label

Job Data:
- `Title`, `Description`, etc.
- Columns: job_title, job_description

### Model Training (`train_models.py`)

**Purpose**: Train ML classifiers on preprocessed data

**Resume Category Classifier**:

```python
from train_models import ModelTrainer

trainer = ModelTrainer(model_dir='models')

# Train on resume data
results = trainer.train_resume_category_classifier(
    training_data,  # DataFrame with 'resume_text' and 'category' columns
    output_name='resume_category_classifier'
)

# Returns: model, vectorizer, evaluation results
```

**Metrics Calculated**:
- Accuracy: What % of predictions were correct
- Precision: How many predicted positives were actually positive
- Recall: How many actual positives were correctly identified
- F1-Score: Harmonic mean of precision & recall

**Trained Models**:
1. **Logistic Regression**: Fast, baseline model
2. **Random Forest**: Ensemble approach, good generalization
3. **Gradient Boosting**: Best performance, slower training

Best model is automatically selected and saved.

**Skill Extraction Models**:

```python
skill_results = trainer.train_skill_extractor(
    training_data,  # DataFrame with 'resume_text' and 'extracted_skills' columns
    output_name='skill_extractor_model'
)

# Creates binary classifiers for each skill
# Top 10 most common skills are trained
```

### Model Integration (`model_integration.py`)

**Purpose**: Load trained models and use them for predictions

**Usage in Application**:

```python
from model_integration import ModelManager, EnsemblePredictor

# Initialize
model_manager = ModelManager('models')

# Predict category
category = model_manager.predict_category(resume_text)
# Returns: {'category': 'Data Scientist', 'confidence': 0.92}

# Predict skills
skills = model_manager.predict_skills(resume_text)
# Returns: {'Python': 85.5, 'Machine Learning': 78.2, ...}

# Ensemble prediction (combines rule-based + ML)
predictor = EnsemblePredictor(job_matcher, model_manager)
top_jobs = predictor.predict_top_jobs(resume_text, jobs_df, top_n=10)

# With skill gap analysis
gap = predictor.get_skill_gap(resume_text, target_job_desc, all_skills)
```

**Scoring Formula**:

Final Job Match Score = (Rule-Based × 0.6) + (ML Enhancement × 0.4)

Where:
- **Rule-Based**: TF-IDF similarity + Skill matching (existing algorithm)
- **ML Enhancement**: Category match bonus + Skill prediction match

## Files Generated

After running `complete_workflow.py`, you'll have:

### Training Data
- `data/training_dataset.csv` - Preprocessed, ready for training

### Trained Models
- `models/resume_category_classifier.pkl` - Category classifier
- `models/resume_category_classifier_vectorizer.pkl` - TF-IDF vectorizer
- `models/skill_extractor_model_models.pkl` - Skill classifiers (binary)
- `models/skill_extractor_model_vectorizer.pkl` - Skill vectorizer

### Reports
- `models/training_report.txt` - Detailed training metrics

## Troubleshooting

### Issue: "No Kaggle datasets found"

**Solution**:
```bash
# 1. Download datasets using Kaggle CLI
kaggle datasets download -d jillanisoftball/resume-data
kaggle datasets download -d snehaanbhawal/resume-nlp

# 2. Extract to correct location
mkdir -p data/kaggle_datasets
unzip -q ResumesDataset.zip -d data/kaggle_datasets/
unzip -q Resume.zip -d data/kaggle_datasets/

# 3. Run workflow again
python complete_workflow.py
```

### Issue: "Memory Error during training"

**Solution**: Reduce dataset size or features
```python
# In complete_workflow.py, limit training data
training_data = training_data.head(5000)  # Use subset
```

### Issue: "Low accuracy scores"

**Possible causes**:
1. Too few training samples (need ≥100 per category)
2. Imbalanced dataset (some categories underrepresented)
3. Noisy or inconsistent labels

**Solutions**:
1. Download more datasets
2. Use `shuffle=True` and `stratified=True` in train_test_split
3. Clean labels in source CSV

### Issue: "Models not found when running app.py"

**Solution**:
```bash
# Train models first
python complete_workflow.py

# Then run app
streamlit run app.py
```

App will use rule-based matching if models not found.

## Performance Benchmarks

**Expected Results** (based on Kaggle datasets):

| Metric | Value |
|--------|-------|
| Category Classifier Accuracy | 75-85% |
| Category Classifier F1-Score | 0.70-0.82 |
| Skill Extraction Accuracy | 80-90% |
| Job Recommendation NDCG@10 | 0.65-0.75 |

Actual results depend on:
- Dataset quality and size
- Category/skill distribution
- Resume diversity

## Advanced Usage

### Using Only Specific Datasets

```python
from data.data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor()

# Load and process only Udacity dataset
resumes = preprocessor.load_resume_data_udacity('data/kaggle_datasets/ResumesDataset.csv')
clean = preprocessor.standardize_resume_columns(resumes)
training = preprocessor.create_training_dataset(clean)
training.to_csv('data/training_dataset.csv', index=False)
```

### Custom Model Configuration

```python
from train_models import ModelTrainer
from sklearn.ensemble import ExtraTreesClassifier

trainer = ModelTrainer(model_dir='models')

# Add custom model to comparison
models['Extra Trees'] = ExtraTreesClassifier(n_estimators=150)
```

### Retraining with New Data

```bash
# Add more Kaggle datasets to data/kaggle_datasets/
# Run workflow again - it will merge with existing data
python complete_workflow.py
```

## Integration with Web App

The web app (`app.py`) automatically:
1. Checks if trained models exist
2. Loads models using `ModelManager`
3. Falls back to rule-based matching if models unavailable
4. Uses `EnsemblePredictor` for better recommendations

**Enable ML Features**:
```python
# In app.py
from model_integration import get_ensemble_predictor

predictor = get_ensemble_predictor(job_matcher)
top_jobs = predictor.predict_top_jobs(resume_text, jobs_df)
```

## Model Maintenance

### Retraining Schedule

Recommended retraining when:
- New Kaggle datasets become available
- Model accuracy drops below 70%
- New job categories are added
- Significant shift in job market

### Versioning

```bash
# Save model with timestamp
cp models/resume_category_classifier.pkl backup/resume_classifier_v2_2024.pkl

# Compare models
python evaluate_models.py
```

## Next Steps

1. **Download Datasets**: Follow [KAGGLE_DOWNLOAD_GUIDE.md](KAGGLE_DOWNLOAD_GUIDE.md)
2. **Run Workflow**: Execute `python complete_workflow.py`
3. **Check Results**: Review `models/training_report.txt`
4. **Test App**: Start with `streamlit run app.py`
5. **Upload Resumes**: Try with sample resumes in `SAMPLE_RESUME_*.txt`

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review training report: `models/training_report.txt`
3. Check data statistics: `data/training_dataset.csv`
4. Test raw preprocessing: `python -c "from data.data_preprocessing import DataPreprocessor; print(DataPreprocessor().get_dataset_statistics(...))"`

## Summary

The ML training pipeline transforms raw Kaggle data into a powerful resume screening system with:
- ✅ Automated category detection
- ✅ Smart skill extraction
- ✅ Enhanced job recommendations
- ✅ Ensemble predictions combining rule-based and ML approaches
- ✅ Comprehensive evaluation metrics

All integrated seamlessly into the Streamlit web application!
