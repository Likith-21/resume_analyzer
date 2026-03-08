"""
Data Preprocessing & Cleaning Script
Prepares Kaggle datasets for model training
"""

import pandas as pd
import numpy as np
import os
import re
from pathlib import Path


class DataPreprocessor:
    """Preprocesses and cleans resume and job data from Kaggle"""
    
    def __init__(self, base_path='data/kaggle_datasets'):
        """Initialize with Kaggle datasets path"""
        self.base_path = base_path
        self.resume_data = None
        self.job_data = None
        self.salary_data = None
        
    def load_resume_data_udacity(self, filepath):
        """Load Udacity resume dataset"""
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Loaded Udacity resume data: {len(df)} records")
            print(f"   Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"❌ Error loading Udacity data: {e}")
            return None
    
    def load_resume_data_nlp(self, filepath):
        """Load NLP resume dataset"""
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Loaded NLP resume data: {len(df)} records")
            print(f"   Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"❌ Error loading NLP data: {e}")
            return None
    
    def load_job_data(self, filepath):
        """Load job descriptions dataset"""
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Loaded job data: {len(df)} records")
            print(f"   Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"❌ Error loading job data: {e}")
            return None
    
    def load_salary_data(self, filepath):
        """Load salary dataset"""
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Loaded salary data: {len(df)} records")
            print(f"   Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"❌ Error loading salary data: {e}")
            return None
    
    def clean_resume_text(self, text):
        """Clean resume text"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s\-]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def standardize_resume_columns(self, df, 
                                   resume_col='resume',
                                   category_col='category'):
        """Standardize resume data columns"""
        try:
            # Find resume column (case-insensitive)
            resume_column = None
            for col in df.columns:
                if 'resume' in col.lower() or 'text' in col.lower():
                    resume_column = col
                    break
            
            # Find category column
            category_column = None
            for col in df.columns:
                if 'category' in col.lower() or 'class' in col.lower():
                    category_column = col
                    break
            
            if resume_column is None or category_column is None:
                print(f"⚠️  Could not find standard columns")
                print(f"   Found columns: {df.columns.tolist()}")
                return df
            
            # Create standardized dataframe
            standardized = pd.DataFrame()
            standardized['resume_text'] = df[resume_column].apply(self.clean_resume_text)
            standardized['category'] = df[category_column]
            
            # Remove duplicates and empty resumes
            standardized = standardized[standardized['resume_text'].str.len() > 50]
            standardized = standardized.drop_duplicates(subset=['resume_text'])
            
            print(f"✅ Standardized resume data: {len(standardized)} records after cleaning")
            
            return standardized
        except Exception as e:
            print(f"❌ Error standardizing data: {e}")
            return df
    
    def standardize_job_columns(self, df,
                               title_col='title',
                               description_col='description'):
        """Standardize job data columns"""
        try:
            # Find relevant columns
            job_columns = {}
            
            for col in df.columns:
                col_lower = col.lower()
                if 'title' in col_lower:
                    job_columns['title'] = col
                elif 'description' in col_lower or 'description' in col_lower:
                    job_columns['description'] = col
                elif 'company' in col_lower:
                    job_columns['company'] = col
                elif 'location' in col_lower:
                    job_columns['location'] = col
            
            # Create standardized dataframe
            standardized = pd.DataFrame()
            standardized['job_title'] = df[job_columns.get('title', df.columns[0])]
            standardized['job_description'] = df[job_columns.get('description', df.columns[1])]
            standardized['company'] = df[job_columns.get('company', 'Unknown')]
            standardized['location'] = df[job_columns.get('location', 'Unknown')]
            
            # Clean text
            standardized['job_description'] = standardized['job_description'].apply(
                lambda x: self.clean_resume_text(x) if pd.notna(x) else ""
            )
            
            # Remove duplicates
            standardized = standardized.drop_duplicates(subset=['job_description'])
            
            print(f"✅ Standardized job data: {len(standardized)} records after cleaning")
            
            return standardized
        except Exception as e:
            print(f"❌ Error standardizing job data: {e}")
            return df
    
    def extract_skills_from_resume(self, resume_text, skills_list):
        """Extract skills from resume text"""
        from data.skills_database import get_all_skills
        
        if skills_list is None:
            skills_list = get_all_skills()
        
        found_skills = []
        resume_lower = str(resume_text).lower()
        
        for skill in skills_list:
            skill_lower = skill.lower()
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_lower):
                found_skills.append(skill)
        
        return ', '.join(found_skills) if found_skills else ""
    
    def create_training_dataset(self, resume_df, output_path='data/training_dataset.csv'):
        """Create final training dataset with extracted skills"""
        try:
            print("\n🔄 Creating training dataset...")
            
            from data.skills_database import get_all_skills
            skills_list = get_all_skills()
            
            # Add extracted skills
            resume_df['extracted_skills'] = resume_df['resume_text'].apply(
                lambda x: self.extract_skills_from_resume(x, skills_list)
            )
            
            # Save training dataset
            resume_df.to_csv(output_path, index=False)
            print(f"✅ Training dataset saved: {output_path}")
            print(f"   Records: {len(resume_df)}")
            print(f"   Columns: {resume_df.columns.tolist()}")
            
            return resume_df
        except Exception as e:
            print(f"❌ Error creating training dataset: {e}")
            return None
    
    def get_dataset_statistics(self, df, name="Dataset"):
        """Get statistics about the dataset"""
        print(f"\n📊 {name} Statistics:")
        print(f"   Total records: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Memory usage: {df.memory_usage().sum() / 1024**2:.2f} MB")
        
        if 'category' in df.columns:
            print(f"   Categories: {df['category'].unique().tolist()}")
            print(f"   Distribution: {df['category'].value_counts().to_dict()}")
        
        return {
            'records': len(df),
            'columns': len(df.columns),
            'memory_mb': df.memory_usage().sum() / 1024**2
        }


def merge_datasets(resume_df, existing_resume_df=None):
    """Merge Kaggle resume data with existing data"""
    try:
        print("\n🔄 Merging datasets...")
        
        if existing_resume_df is not None:
            merged = pd.concat([resume_df, existing_resume_df], ignore_index=True)
            merged = merged.drop_duplicates(subset=['resume_text'])
            print(f"✅ Merged dataset: {len(merged)} unique records")
            return merged
        
        return resume_df
    except Exception as e:
        print(f"❌ Error merging datasets: {e}")
        return resume_df


def main():
    """Main preprocessing pipeline"""
    print("=" * 60)
    print("  DATA PREPROCESSING PIPELINE FOR KAGGLE DATASETS")
    print("=" * 60)
    
    preprocessor = DataPreprocessor()
    
    # Example: Load Udacity resume data
    print("\n1️⃣  Loading Resume Data from Kaggle...")
    resume_file = 'data/kaggle_datasets/resume-data/Resume.csv'
    if os.path.exists(resume_file):
        resume_df = preprocessor.load_resume_data_udacity(resume_file)
        
        if resume_df is not None:
            # Standardize columns
            standardized = preprocessor.standardize_resume_columns(resume_df)
            
            # Get statistics
            preprocessor.get_dataset_statistics(standardized, "Resume Data")
            
            # Create training dataset
            training_df = preprocessor.create_training_dataset(standardized)
            
            print("\n✅ Data preprocessing complete!")
    else:
        print(f"❌ File not found: {resume_file}")
        print(f"   Expected path: {resume_file}")
        print(f"   Please download from Kaggle and place in correct folder")


if __name__ == "__main__":
    main()
