"""
Custom Training Script - Using User-Provided Datasets
Trains models on job data (521 jobs) + existing resume data (20 resumes)
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from train_models import ModelTrainer
from data.skills_database import get_all_skills


def load_user_job_data():
    """Load the 521 job postings provided by user"""
    print("\n" + "="*70)
    print("  LOADING USER-PROVIDED DATASETS")
    print("="*70)
    
    job_file = 'data/kaggle_datasets/jobs_dataset.csv'
    
    print(f"\n📊 Loading job dataset: {job_file}")
    jobs_df = pd.read_csv(job_file)
    print(f"   ✅ Loaded {len(jobs_df)} job postings")
    print(f"   Columns: {list(jobs_df.columns)}")
    
    # Rename columns to standard format
    if 'Job Title' in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={
            'Job Title': 'job_title',
            'Description': 'job_description'
        })
    
    return jobs_df


def enhance_jobs_database(new_jobs_df):
    """Save enhanced job database"""
    print(f"\n💾 Saving enhanced job database...")
    
    # Load existing jobs
    existing_jobs = pd.read_csv('data/jobs.csv')
    print(f"   Existing jobs: {len(existing_jobs)}")
    print(f"   New jobs: {len(new_jobs_df)}")
    
    # Combine (keep first 50 from new dataset to avoid too large)
    combined_jobs = pd.concat([
        existing_jobs,
        new_jobs_df.head(50)  # Add 50 most diverse jobs
    ], ignore_index=True)
    
    # Remove duplicates based on title
    combined_jobs = combined_jobs.drop_duplicates(subset=['job_title'], keep='first')
    
    # Save
    combined_jobs.to_csv('data/enhanced_jobs.csv', index=False)
    print(f"   ✅ Saved {len(combined_jobs)} total jobs to enhanced_jobs.csv")
    
    return combined_jobs


def create_training_dataset_from_resumes():
    """Create training dataset from existing resume data"""
    print(f"\n📋 Creating training dataset from existing resumes...")
    
    resume_file = 'data/resume_dataset.csv'
    
    if not os.path.exists(resume_file):
        print(f"   ❌ Resume dataset not found: {resume_file}")
        return None
    
    resumes_df = pd.read_csv(resume_file)
    print(f"   ✅ Loaded {len(resumes_df)} resume profiles")
    print(f"   Columns: {list(resumes_df.columns)}")
    
    # Ensure we have required columns
    required_cols = ['resume_text', 'category']
    
    if 'resume_text' not in resumes_df.columns:
        # Construct resume_text from available columns
        print(f"   🔄 Constructing resume_text from available columns...")
        resumes_df['resume_text'] = (
            resumes_df['category'].fillna('Professional') + ' with ' +
            resumes_df['experience_years'].fillna(0).astype(str) + ' years experience. ' +
            resumes_df['summary'].fillna('') + ' ' +
            'Skills: ' + resumes_df['skills'].fillna('') + '. ' +
            'Education: ' + resumes_df['education'].fillna('') + '. ' +
            'Location: ' + resumes_df['location'].fillna('')
        )
        print(f"   ✅ Constructed resume_text from available columns")
    
    # Check for category
    if 'category' not in resumes_df.columns and 'job_category' in resumes_df.columns:
        resumes_df['category'] = resumes_df['job_category']
    
    # Validate - now both columns should exist
    if 'resume_text' not in resumes_df.columns or 'category' not in resumes_df.columns:
        print(f"   ❌ Required columns still missing after construction")
        return None
    
    print(f"   ✅ Resume data ready with {len(resumes_df)} samples")
    
    # Extract skills from resume text
    from data.skills_database import get_all_skills
    all_skills = get_all_skills()
    
    def extract_skills(text):
        if pd.isna(text):
            return ''
        text_lower = str(text).lower()
        found_skills = [skill for skill in all_skills if skill.lower() in text_lower]
        return ', '.join(found_skills[:10])  # Top 10 skills
    
    print(f"\n🔍 Extracting skills from resumes...")
    resumes_df['extracted_skills'] = resumes_df['resume_text'].apply(extract_skills)
    
    # Save training dataset
    training_file = 'data/training_dataset.csv'
    resumes_df.to_csv(training_file, index=False)
    print(f"   ✅ Saved training dataset: {training_file}")
    
    # Statistics
    print(f"\n📊 Training Dataset Statistics:")
    print(f"   Total samples: {len(resumes_df)}")
    print(f"   Categories: {resumes_df['category'].nunique()}")
    print(f"   Category distribution:")
    for cat, count in resumes_df['category'].value_counts().items():
        print(f"      {cat}: {count}")
    
    return resumes_df


def augment_training_data(resumes_df, jobs_df):
    """
    Create synthetic resumes from job descriptions to increase training data
    """
    print(f"\n🔄 Augmenting training data with synthetic resumes...")
    
    synthetic_resumes = []
    
    # Group similar job titles into broader categories
    category_mapping = {
        'data analyst': 'Data Analyst',
        'business analyst': 'Data Analyst', 
        'data scientist': 'Data Scientist',
        'machine learning': 'Data Scientist',
        'ml engineer': 'Data Scientist',
        'software engineer': 'Software Engineer',
        'developer': 'Software Engineer',
        'devops': 'DevOps Engineer',
        'web developer': 'Web Developer',
        'frontend': 'Frontend Developer',
        'backend': 'Backend Developer',
        'data engineer': 'Data Engineer',
        'database': 'Database Administrator',
        'cloud': 'Cloud Architect',
        'cybersecurity': 'Cybersecurity Engineer',
        'business intelligence': 'Business Intelligence',
        'product manager': 'Product Manager',
    }
    
    def normalize_category(job_title):
        """Normalize job title to broader category"""
        job_lower = str(job_title).lower()
        for key, category in category_mapping.items():
            if key in job_lower:
                return category
        return 'Software Engineer'  # Default category
    
    # Sample diverse job postings (3 per normalized category)
    jobs_by_category = {}
    for idx, row in jobs_df.iterrows():
        normalized = normalize_category(row['job_title'])
        if normalized not in jobs_by_category:
            jobs_by_category[normalized] = []
        if len(jobs_by_category[normalized]) < 3:  # 3 samples per category
            jobs_by_category[normalized].append(row)
    
    # Create synthetic resumes from job descriptions
    for category, job_rows in jobs_by_category.items():
        for job_row in job_rows:
            desc = job_row['job_description']
            
            # Extract key skills from description
            from data.skills_database import get_all_skills
            all_skills = get_all_skills()
            desc_lower = str(desc).lower()
            found_skills = [skill for skill in all_skills if skill.lower() in desc_lower]
            
            # Create resume text
            resume_text = f"""
            {category} professional with 3-5 years experience.
            Technical Skills: {', '.join(found_skills[:10])}
            Experience working with: {', '.join(found_skills[10:15])}
            Strong background in data analysis, problem solving, and technical implementation.
            Proficient in: {', '.join(found_skills[:7])}
            """
            
            synthetic_resumes.append({
                'resume_text': resume_text,
                'category': category,
                'extracted_skills': ', '.join(found_skills[:10]),
                'synthetic': True
            })
    
    print(f"   ✅ Created {len(synthetic_resumes)} synthetic resumes")
    print(f"   📊 Categories created: {len(jobs_by_category)}")
    
    # Also normalize categories in real resume data
    resumes_df['category'] = resumes_df['category'].apply(normalize_category)
    
    # Combine with real resumes
    synthetic_df = pd.DataFrame(synthetic_resumes)
    augmented_df = pd.concat([resumes_df, synthetic_df], ignore_index=True)
    
    # Show distribution
    print(f"\n   📈 Category distribution after augmentation:")
    for cat, count in augmented_df['category'].value_counts().head(10).items():
        print(f"      {cat}: {count} samples")
    
    # Save augmented dataset
    augmented_df.to_csv('data/augmented_training_dataset.csv', index=False)
    print(f"   ✅ Saved augmented dataset: {len(augmented_df)} total samples")
    
    return augmented_df


def train_models_on_data(training_data):
    """Train ML models on the prepared data"""
    print("\n" + "="*70)
    print("  TRAINING ML MODELS")
    print("="*70)
    
    if training_data is None or len(training_data) == 0:
        print("❌ No training data available")
        return False
    
    # Initialize trainer
    trainer = ModelTrainer(model_dir='models')
    
    # Train resume category classifier
    print(f"\n1️⃣  Training Resume Category Classifier...")
    model_results = trainer.train_resume_category_classifier(
        training_data,
        output_name='resume_category_classifier'
    )
    
    if model_results is None:
        print("❌ Failed to train category classifier")
        return False
    
    # Train skill extractor
    print(f"\n2️⃣  Training Skill Extraction Models...")
    skill_results = trainer.train_skill_extractor(
        training_data,
        output_name='skill_extractor_model'
    )
    
    # Evaluate
    print(f"\n3️⃣  Evaluating Models...")
    trainer.evaluate_models(model_results)
    
    # Save comprehensive report
    print(f"\n4️⃣  Saving Training Report...")
    trainer.save_training_report(training_data, model_results, skill_results)
    
    return True


def main():
    """Main execution flow"""
    print("\n" + "="*70)
    print("  🤖 CUSTOM TRAINING PIPELINE - USER PROVIDED DATA")
    print("="*70)
    print("\nUsing:")
    print("  • 521 job postings from data.csv")
    print("  • 20 resume profiles from resume_dataset.csv")
    print("  • Synthetic resumes generated from job descriptions")
    print("="*70)
    
    try:
        # Step 1: Load user's job data
        jobs_df = load_user_job_data()
        
        # Step 2: Enhance jobs database
        enhanced_jobs = enhance_jobs_database(jobs_df)
        
        # Step 3: Create training dataset from resumes
        training_data = create_training_dataset_from_resumes()
        
        if training_data is None:
            print("\n❌ Failed to create training dataset")
            return False
        
        # Step 4: Augment with synthetic data
        augmented_data = augment_training_data(training_data, jobs_df)
        
        # Step 5: Train models
        success = train_models_on_data(augmented_data)
        
        if success:
            print("\n" + "="*70)
            print("✅ CUSTOM TRAINING COMPLETE!")
            print("="*70)
            print("\nFiles created:")
            print("  • data/enhanced_jobs.csv - 70+ job postings")
            print("  • data/augmented_training_dataset.csv - Training data")
            print("  • models/resume_category_classifier.pkl - Trained model")
            print("  • models/skill_extractor_model_models.pkl - Skill models")
            print("  • models/training_report.txt - Performance metrics")
            print("\nNext steps:")
            print("  1. Review training results: cat models/training_report.txt")
            print("  2. Start web app: streamlit run app.py")
            print("  3. Upload resumes and test ML-enhanced recommendations!")
            print("="*70)
            return True
        else:
            print("\n⚠️  Training completed with warnings")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
