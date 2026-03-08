"""
Complete ML Workflow Orchestrator
Handles data preprocessing and model training in sequence
"""

import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.data_preprocessing import DataPreprocessor
import pandas as pd


class MLWorkflow:
    """Orchestrates complete ML pipeline"""
    
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.kaggle_data_dir = 'data/kaggle_datasets'
    
    def step1_setup_directories(self):
        """Create required directories"""
        print("\n" + "="*60)
        print("STEP 1: SETTING UP DIRECTORIES")
        print("="*60)
        
        os.makedirs(self.kaggle_data_dir, exist_ok=True)
        os.makedirs('models', exist_ok=True)
        
        print(f"✅ Created '{self.kaggle_data_dir}'")
        print(f"✅ Created 'models' directory")
        
        print("\n📁 Place your Kaggle datasets in:")
        print(f"   {os.path.abspath(self.kaggle_data_dir)}/")
    
    def step2_load_kaggle_data(self):
        """Load data from Kaggle datasets"""
        print("\n" + "="*60)
        print("STEP 2: LOADING KAGGLE DATA")
        print("="*60)
        
        all_resumes = []
        
        # Define expected Kaggle files
        kaggle_sources = {
            'Udacity Resume Dataset': [
                self.kaggle_data_dir + '/ResumesDataset.csv',
                self.kaggle_data_dir + '/udacity_resumes.csv',
                self.kaggle_data_dir + '/udacity_resume.csv'
            ],
            'NLP Resume Dataset': [
                self.kaggle_data_dir + '/Resume.csv',
                self.kaggle_data_dir + '/resume.csv',
                self.kaggle_data_dir + '/nlp_resume.csv'
            ],
            'Job Descriptions': [
                self.kaggle_data_dir + '/jobs.csv',
                self.kaggle_data_dir + '/job_descriptions.csv',
                self.kaggle_data_dir + '/job_postings.csv'
            ]
        }
        
        print("\n🔍 Looking for Kaggle datasets...")
        
        for source, possible_paths in kaggle_sources.items():
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"\n✅ Found: {source}")
                    print(f"   File: {path}")
                    try:
                        df = pd.read_csv(path)
                        print(f"   Records: {len(df)}")
                        print(f"   Columns: {list(df.columns)[:5]}...")
                        
                        # Load based on source
                        if 'Udacity' in source:
                            all_resumes.append(self.preprocessor.load_resume_data_udacity(path))
                        elif 'NLP' in source:
                            all_resumes.append(self.preprocessor.load_resume_data_nlp(path))
                        
                    except Exception as e:
                        print(f"   ⚠️  Error loading: {e}")
                    break
        
        if not all_resumes:
            print("\n⚠️  No Kaggle datasets found!")
            print("\nTo proceed, download datasets from Kaggle:")
            print("  1. Run: kaggle datasets download -d jillanisoftball/resume-data")
            print("  2. Run: kaggle datasets download -d snehaanbhawal/resume-nlp")
            print("  3. Run: kaggle datasets download -d kashnitsky/job-salary-data")
            print(f"  4. Extract to: {os.path.abspath(self.kaggle_data_dir)}/")
            return None
        
        print(f"\n✅ Loaded {len(all_resumes)} resume sources")
        return pd.concat(all_resumes, ignore_index=True) if all_resumes else None
    
    def step3_preprocess_data(self, kaggle_resumes):
        """Clean and standardize data"""
        print("\n" + "="*60)
        print("STEP 3: PREPROCESSING DATA")
        print("="*60)
        
        if kaggle_resumes is None:
            print("⚠️  Skipping - no Kaggle data loaded")
            return None
        
        print(f"\nStarting with {len(kaggle_resumes)} records")
        
        # Standardize columns
        print("\n🔄 Standardizing resume columns...")
        cleaned_resumes = self.preprocessor.standardize_resume_columns(kaggle_resumes)
        print(f"✅ Cleaned {len(cleaned_resumes)} records")
        
        # Extract skills
        print("\n🔍 Extracting skills from resumes...")
        cleaned_resumes = cleaned_resumes.copy()
        cleaned_resumes['extracted_skills'] = cleaned_resumes['resume_text'].apply(
            lambda x: self.preprocessor.extract_skills_from_resume(str(x)) 
            if pd.notna(x) else ''
        )
        print(f"✅ Extracted skills")
        
        # Get statistics
        print("\n📊 Dataset Statistics:")
        stats = self.preprocessor.get_dataset_statistics(cleaned_resumes)
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return cleaned_resumes
    
    def step4_create_training_data(self, cleaned_resumes):
        """Create final training dataset"""
        print("\n" + "="*60)
        print("STEP 4: CREATING TRAINING DATASET")
        print("="*60)
        
        if cleaned_resumes is None:
            print("⚠️  Skipping - no cleaned data")
            # Use existing dataset if available
            if os.path.exists('data/resume_dataset.csv'):
                print("✅ Using existing resume_dataset.csv")
                return pd.read_csv('data/resume_dataset.csv')
            return None
        
        print(f"\nProcessing {len(cleaned_resumes)} records...")
        
        # Create training dataset
        training_data = self.preprocessor.create_training_dataset(cleaned_resumes)
        
        print(f"✅ Created training dataset: {len(training_data)} records")
        
        # Save
        output_path = 'data/training_dataset.csv'
        training_data.to_csv(output_path, index=False)
        print(f"✅ Saved: {output_path}")
        
        # Show sample
        print("\n📋 Sample records:")
        print(training_data.head(2).to_string())
        
        return training_data
    
    def step5_train_models(self, training_data):
        """Train ML models"""
        print("\n" + "="*60)
        print("STEP 5: TRAINING MODELS")
        print("="*60)
        
        if training_data is None or len(training_data) == 0:
            print("❌ No training data available")
            return False
        
        try:
            from train_models import ModelTrainer
            
            trainer = ModelTrainer()
            
            # Train classifier
            model_results = trainer.train_resume_category_classifier(training_data)
            
            # Train skill extractor
            skill_results = trainer.train_skill_extractor(training_data)
            
            # Evaluate
            trainer.evaluate_models(model_results)
            
            # Save report
            trainer.save_training_report(training_data, model_results, skill_results)
            
            return True
            
        except Exception as e:
            print(f"❌ Error during training: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_complete_workflow(self):
        """Execute all steps"""
        print("\n" + "="*70)
        print("  🤖 COMPLETE ML WORKFLOW - RESUME SCREENING SYSTEM")
        print("="*70)
        
        # Step 1: Setup
        self.step1_setup_directories()
        
        # Step 2: Load Kaggle data
        kaggle_resumes = self.step2_load_kaggle_data()
        
        # Step 3: Preprocess
        cleaned_resumes = self.step3_preprocess_data(kaggle_resumes)
        
        # Step 4: Create training data
        training_data = self.step4_create_training_data(cleaned_resumes)
        
        # Step 5: Train models
        if training_data is not None and len(training_data) > 0:
            success = self.step5_train_models(training_data)
        else:
            print("\n⚠️  Cannot train without data")
            success = False
        
        # Summary
        print("\n" + "="*70)
        if success:
            print("✅ ML WORKFLOW COMPLETE!")
            print("="*70)
            print("\nModels trained and saved in 'models/' directory")
            print("Next steps:")
            print("  1. Review training results in models/training_report.txt")
            print("  2. Run the web app: streamlit run app.py")
            print("  3. Upload resumes to test the system")
        else:
            print("⚠️  WORKFLOW PARTIALLY COMPLETE")
            print("="*70)
            print("\nStatus:")
            print("  ✅ Data preprocessing setup ready")
            print("  ✅ Training dataset structure created")
            print("  ⚠️  Models not trained (awaiting Kaggle data)")
            print("\nTo complete:")
            print("  1. Download Kaggle datasets (see KAGGLE_DOWNLOAD_GUIDE.md)")
            print("  2. Place in data/kaggle_datasets/ folder")
            print("  3. Run this script again: python complete_workflow.py")
        
        return success


def main():
    """Main entry point"""
    workflow = MLWorkflow()
    workflow.run_complete_workflow()


if __name__ == "__main__":
    main()
