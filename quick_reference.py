"""
Quick Reference Script for ML Model Training & Usage
Demonstrates common usage patterns
"""

# ============================================================================
# EXAMPLE 1: Full Training Pipeline (One Command)
# ============================================================================

def example_complete_training():
    """Run complete training workflow with Kaggle data"""
    from complete_workflow import MLWorkflow
    
    workflow = MLWorkflow()
    workflow.run_complete_workflow()


# ============================================================================
# EXAMPLE 2: Load and Use Trained Models
# ============================================================================

def example_use_trained_models():
    """Load trained models and make predictions"""
    from model_integration import ModelManager
    
    # Load models
    manager = ModelManager('models')
    
    # Check if models are available
    print(f"Models trained: {manager.is_trained}")
    print(f"Stats: {manager.get_model_stats()}")
    
    # Sample resume text
    resume = """
    Data Scientist with 5 years experience
    Skills: Python, Machine Learning, TensorFlow, SQL, Pandas, Scikit-learn
    Education: MS Computer Science
    """
    
    # Predict category
    category = manager.predict_category(resume)
    if category:
        print(f"Predicted Category: {category['category']}")
        print(f"Confidence: {category['confidence']:.1%}")
    
    # Predict skills
    skills = manager.predict_skills(resume)
    if skills:
        print(f"Predicted Skills: {skills}")


# ============================================================================
# EXAMPLE 3: Custom Data Preprocessing
# ============================================================================

def example_custom_preprocessing():
    """Load and preprocess specific Kaggle dataset"""
    from data.data_preprocessing import DataPreprocessor
    import pandas as pd
    
    preprocessor = DataPreprocessor()
    
    # Load Udacity dataset
    df = pd.read_csv('data/kaggle_datasets/ResumesDataset.csv')
    print(f"Raw data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Standardize columns
    df_clean = preprocessor.standardize_resume_columns(df)
    
    # Extract skills
    df_clean['extracted_skills'] = df_clean['resume_text'].apply(
        preprocessor.extract_skills_from_resume
    )
    
    # Create training dataset
    training_data = preprocessor.create_training_dataset(df_clean)
    
    # Save
    training_data.to_csv('data/custom_training_data.csv', index=False)
    print(f"Saved training data: {training_data.shape}")


# ============================================================================
# EXAMPLE 4: Train Specific Models Only
# ============================================================================

def example_train_specific_models():
    """Train individual models"""
    from train_models import ModelTrainer
    import pandas as pd
    
    # Load training data
    training_data = pd.read_csv('data/training_dataset.csv')
    
    trainer = ModelTrainer()
    
    # Train only resume classifier
    print("Training resume classifier...")
    classifier_results = trainer.train_resume_category_classifier(training_data)
    
    # Train only skill extractor
    print("\nTraining skill extractor...")
    skill_results = trainer.train_skill_extractor(training_data)
    
    # Evaluate
    trainer.evaluate_models(classifier_results)
    
    # Save report
    trainer.save_training_report(training_data, classifier_results, skill_results)


# ============================================================================
# EXAMPLE 5: Use with Job Matcher (Ensemble)
# ============================================================================

def example_ensemble_prediction():
    """Combine rule-based and ML predictions"""
    from model_integration import EnsemblePredictor
    from modules.job_matcher import JobMatcher
    import pandas as pd
    
    # Load data
    jobs_df = pd.read_csv('data/jobs.csv')
    
    # Initialize matcher and predictor
    job_matcher = JobMatcher()
    from model_integration import ModelManager
    predictor = EnsemblePredictor(job_matcher, ModelManager())
    
    # Sample resume
    resume_text = """
    Senior Software Engineer
    Python, Java, Kubernetes, Docker
    10 years experience
    """
    
    # Get top matching jobs
    top_jobs = predictor.predict_top_jobs(resume_text, jobs_df, top_n=5)
    
    for job in top_jobs:
        print(f"\nJob: {job['job_title']}")
        print(f"Match: {job.get('match_percentage', 0):.1f}%")
        print(f"ML Score: {job.get('ml_score', 0):.1f}")
        print(f"Combined: {job.get('combined_score', 0):.1f}")


# ============================================================================
# EXAMPLE 6: Evaluate Model Performance
# ============================================================================

def example_evaluate_models():
    """Load and evaluate trained models"""
    import joblib
    import pandas as pd
    from sklearn.metrics import accuracy_score, classification_report
    from model_integration import ModelManager
    
    # Load test data
    test_data = pd.read_csv('data/test_dataset.csv')  # If available
    
    manager = ModelManager()
    
    if not manager.is_trained:
        print("No trained models found")
        return
    
    # Batch predict categories
    predictions = []
    for resume in test_data['resume_text']:
        pred = manager.predict_category(resume)
        if pred:
            predictions.append(pred['category'])
        else:
            predictions.append(None)
    
    # Calculate accuracy
    accuracy = accuracy_score(test_data['category'], predictions)
    print(f"Accuracy: {accuracy:.4f}")
    
    # Classification report
    print(classification_report(test_data['category'], predictions))


# ============================================================================
# EXAMPLE 7: Integrate with Streamlit App
# ============================================================================

def example_streamlit_integration():
    """Show how to integrate in Streamlit app"""
    code = """
    # In app.py
    import streamlit as st
    from model_integration import get_ensemble_predictor
    from modules.job_matcher import JobMatcher
    import pandas as pd
    
    # Load data
    jobs_df = pd.read_csv('data/jobs.csv')
    job_matcher = JobMatcher()
    
    # Create predictor
    predictor = get_ensemble_predictor(job_matcher)
    
    # In your function
    def show_job_recommendations(resume_text):
        # Use ensemble predictor for better accuracy
        top_jobs = predictor.predict_top_jobs(resume_text, jobs_df, top_n=10)
        
        for idx, job in enumerate(top_jobs, 1):
            st.write(f"{idx}. {job['job_title']}")
            st.metric("Match Score", f"{job.get('match_percentage', 0):.1f}%")
            if 'ml_score' in job:
                st.metric("ML Enhancement", f"{job['ml_score']:.1f}")
    """
    print(code)


# ============================================================================
# EXAMPLE 8: Process New Resume and Get Full Analysis
# ============================================================================

def example_full_resume_analysis():
    """Complete analysis pipeline for a resume"""
    from model_integration import ModelManager, EnsemblePredictor
    from modules.job_matcher import JobMatcher
    from modules.resume_parser import ResumeParser
    from modules.skill_extractor import SkillExtractor
    import pandas as pd
    
    # Parse resume
    parser = ResumeParser()
    resume_text = parser.extract_text_from_pdf('resume.pdf')
    
    # Extract info
    extractor = SkillExtractor()
    skills = extractor.extract_skills(resume_text)
    experience_years = extractor.estimate_experience_years(resume_text)
    
    print(f"📄 Resume Analysis")
    print(f"  Skills found: {len(skills)}")
    print(f"  Experience: {experience_years} years")
    
    # ML predictions
    manager = ModelManager()
    category = manager.predict_category(resume_text)
    if category:
        print(f"  Category: {category['category']} ({category['confidence']:.1%})")
    
    # Job recommendations
    jobs_df = pd.read_csv('data/jobs.csv')
    job_matcher = JobMatcher()
    predictor = EnsemblePredictor(job_matcher, manager)
    
    top_jobs = predictor.predict_top_jobs(resume_text, jobs_df, top_n=10)
    print(f"\n👼 Top 10 Matching Jobs:")
    for idx, job in enumerate(top_jobs, 1):
        print(f"  {idx}. {job['job_title']} ({job.get('match_percentage', 0):.1f}% match)")


# ============================================================================
# MAIN - Run Examples
# ============================================================================

if __name__ == "__main__":
    import sys
    
    examples = {
        '1': ('Complete Training', example_complete_training),
        '2': ('Use Trained Models', example_use_trained_models),
        '3': ('Custom Preprocessing', example_custom_preprocessing),
        '4': ('Train Specific Models', example_train_specific_models),
        '5': ('Ensemble Prediction', example_ensemble_prediction),
        '6': ('Evaluate Models', example_evaluate_models),
        '7': ('Streamlit Integration', example_streamlit_integration),
        '8': ('Full Resume Analysis', example_full_resume_analysis),
    }
    
    print("\n" + "="*60)
    print("  ML QUICK REFERENCE EXAMPLES")
    print("="*60)
    print("\nChoose an example to run:")
    
    for key, (desc, _) in examples.items():
        print(f"  {key}. {desc}")
    
    print("\nUsage: python quick_reference.py <example_number>")
    print("       python quick_reference.py 1")
    print("\nOr import and use directly:")
    print("  from quick_reference import example_use_trained_models")
    print("  example_use_trained_models()")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in examples:
            print(f"\n▶️  Running: {examples[choice][0]}")
            print("-" * 60)
            try:
                examples[choice][1]()
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"❌ Invalid choice: {choice}")
    else:
        print("\n➡️  Tip: Run 'python quick_reference.py 1' to execute example 1")
