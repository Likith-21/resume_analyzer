"""
Machine Learning Model Training Pipeline
Trains models on Kaggle datasets for resume classification and skill extraction
"""

import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score


class ModelTrainer:
    """Trains ML models on resume and job data"""
    
    def __init__(self, model_dir='models'):
        """Initialize trainer with model directory"""
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        self.resume_classifier = None
        self.tfidf_vectorizer = None
        self.skill_classifier = None
    
    def train_resume_category_classifier(self, 
                                        training_data,
                                        output_name='resume_category_classifier'):
        """
        Train a classifier to predict resume category
        
        Expected columns in training_data:
        - resume_text: The resume content
        - category: The job category (label)
        """
        print("\n" + "="*60)
        print("  TRAINING RESUME CATEGORY CLASSIFIER")
        print("="*60)
        
        try:
            # Prepare data
            X = training_data['resume_text']
            y = training_data['category']
            
            print(f"\n📊 Dataset Statistics:")
            print(f"   Total samples: {len(X)}")
            print(f"   Categories: {len(y.unique())}")
            print(f"   Category distribution:\n{y.value_counts()}")
            
            # Remove any NaN values
            valid_mask = X.notna() & y.notna()
            X = X[valid_mask]
            y = y[valid_mask]
            
            print(f"   After cleaning: {len(X)} samples")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y if len(y) > 50 else None
            )
            
            print(f"\n📈 Train-Test Split:")
            print(f"   Training set: {len(X_train)} samples")
            print(f"   Test set: {len(X_test)} samples")
            
            # Vectorize text
            print(f"\n🔄 Vectorizing text with TF-IDF...")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            X_train_tfidf = self.tfidf_vectorizer.fit_transform(X_train)
            X_test_tfidf = self.tfidf_vectorizer.transform(X_test)
            
            print(f"   ✅ Vectorization complete")
            print(f"   Feature dimension: {X_train_tfidf.shape[1]}")
            
            # Train multiple models and compare
            print(f"\n🤖 Training classifiers...")
            
            models = {
                'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
            }
            
            results = {}
            best_model = None
            best_score = 0
            best_name = None
            
            for model_name, model in models.items():
                print(f"\n   Training {model_name}...")
                model.fit(X_train_tfidf, y_train)
                
                # Predict
                y_pred = model.predict(X_test_tfidf)
                y_pred_proba = model.predict_proba(X_test_tfidf)
                
                # Evaluate
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                
                results[model_name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
                
                print(f"      Accuracy:  {accuracy:.4f}")
                print(f"      Precision: {precision:.4f}")
                print(f"      Recall:    {recall:.4f}")
                print(f"      F1-Score:  {f1:.4f}")
                
                if f1 > best_score:
                    best_score = f1
                    best_model = model
                    best_name = model_name
            
            print(f"\n🏆 Best Model: {best_name} (F1-Score: {best_score:.4f})")
            
            # Save best model
            model_path = os.path.join(self.model_dir, f'{output_name}.pkl')
            joblib.dump(best_model, model_path)
            print(f"✅ Model saved: {model_path}")
            
            # Save vectorizer
            vectorizer_path = os.path.join(self.model_dir, f'{output_name}_vectorizer.pkl')
            joblib.dump(self.tfidf_vectorizer, vectorizer_path)
            print(f"✅ Vectorizer saved: {vectorizer_path}")
            
            self.resume_classifier = best_model
            
            # Print classification report
            print(f"\n📊 Detailed Classification Report:")
            print(classification_report(y_test, y_pred))
            
            return {
                'model': best_model,
                'vectorizer': self.tfidf_vectorizer,
                'results': results,
                'best_model': best_name,
                'best_score': best_score
            }
            
        except Exception as e:
            print(f"❌ Error training classifier: {e}")
            return None
    
    def train_skill_extractor(self,
                             training_data,
                             output_name='skill_extractor_model'):
        """
        Train model to extract skills from resume text
        Creates skill labels from extracted_skills column
        """
        print("\n" + "="*60)
        print("  TRAINING SKILL EXTRACTION MODEL")
        print("="*60)
        
        try:
            # Create binary labels for skills (multi-label classification)
            from data.skills_database import get_all_skills
            all_skills = get_all_skills()
            
            print(f"\n🔧 Skill Database:")
            print(f"   Total skills: {len(all_skills)}")
            print(f"   Top 20 skills: {all_skills[:20]}")
            
            # Get most common skills for easier training
            skill_counts = {}
            for idx, row in training_data.iterrows():
                if pd.notna(row.get('extracted_skills', '')):
                    skills = str(row['extracted_skills']).split(', ')
                    for skill in skills:
                        skill = skill.strip()
                        if skill:
                            skill_counts[skill] = skill_counts.get(skill, 0) + 1
            
            # Top skills to focus on
            top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]
            top_skill_list = [s[0] for s in top_skills]
            
            print(f"\n📈 Top Skills in Dataset:")
            for skill, count in top_skills[:10]:
                print(f"   {skill}: {count} resumes")
            
            # Create training data for skill classification
            X = training_data['resume_text']
            
            # Vectorize
            print(f"\n🔄 Vectorizing text...")
            vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
            X_tfidf = vectorizer.fit_transform(X)
            print(f"   ✅ Features: {X_tfidf.shape[1]}")
            
            # Train separate classifier for top skills
            print(f"\n🤖 Training skill classifiers...")
            
            skill_models = {}
            for skill in top_skill_list[:10]:  # Train on top 10 skills
                # Create binary label for this skill
                y = training_data['extracted_skills'].apply(
                    lambda x: 1 if skill in str(x) else 0
                )
                
                if len(y[y==1]) < 5:  # Skip if too few positive examples
                    continue
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X_tfidf, y, test_size=0.2, random_state=42
                )
                
                model = LogisticRegression(max_iter=1000, random_state=42)
                model.fit(X_train, y_train)
                
                accuracy = accuracy_score(y_test, model.predict(X_test))
                skill_models[skill] = {
                    'model': model,
                    'accuracy': accuracy
                }
                
                print(f"   {skill}: Accuracy {accuracy:.4f}")
            
            # Save models
            models_path = os.path.join(self.model_dir, f'{output_name}_models.pkl')
            joblib.dump(skill_models, models_path)
            print(f"\n✅ Skill models saved: {models_path}")
            
            vectorizer_path = os.path.join(self.model_dir, f'{output_name}_vectorizer.pkl')
            joblib.dump(vectorizer, vectorizer_path)
            print(f"✅ Vectorizer saved: {vectorizer_path}")
            
            return {
                'models': skill_models,
                'vectorizer': vectorizer,
                'top_skills': top_skill_list
            }
            
        except Exception as e:
            print(f"❌ Error training skill extractor: {e}")
            return None
    
    def evaluate_models(self, model_results):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("  MODEL EVALUATION SUMMARY")
        print("="*60)
        
        if model_results and 'results' in model_results:
            print("\n📊 Classifier Performance:")
            for model_name, metrics in model_results['results'].items():
                print(f"\n{model_name}:")
                for metric, value in metrics.items():
                    print(f"   {metric.capitalize()}: {value:.4f}")
    
    def save_training_report(self, training_data, model_results, skill_results):
        """Save comprehensive training report"""
        report_path = os.path.join(self.model_dir, 'training_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("  MACHINE LEARNING MODEL TRAINING REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Dataset info
            f.write("DATASET INFORMATION\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total records: {len(training_data)}\n")
            if 'category' in training_data.columns:
                f.write(f"Categories: {training_data['category'].nunique()}\n")
                f.write("Category distribution:\n")
                for cat, count in training_data['category'].value_counts().items():
                    f.write(f"  {cat}: {count}\n")
            
            # Resume classifier results
            if model_results:
                f.write("\n\nRESUME CATEGORY CLASSIFIER\n")
                f.write("-" * 60 + "\n")
                f.write(f"Best Model: {model_results['best_model']}\n")
                f.write(f"Best F1-Score: {model_results['best_score']:.4f}\n")
                for model_name, metrics in model_results['results'].items():
                    f.write(f"\n{model_name}:\n")
                    for metric, value in metrics.items():
                        f.write(f"  {metric}: {value:.4f}\n")
            
            # Skill extractor results
            if skill_results:
                f.write("\n\nSKILL EXTRACTOR MODEL\n")
                f.write("-" * 60 + "\n")
                f.write(f"Top skills trained: {len(skill_results['models'])}\n")
                for skill, info in skill_results['models'].items():
                    f.write(f"  {skill}: {info['accuracy']:.4f} accuracy\n")
        
        print(f"\n✅ Training report saved: {report_path}")


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("  ML MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # Load training data
    print("\n1️⃣  Loading training data...")
    training_file = 'data/training_dataset.csv'
    
    if os.path.exists(training_file):
        training_data = pd.read_csv(training_file)
        print(f"✅ Loaded: {len(training_data)} records")
    else:
        print(f"⚠️  Training data not found: {training_file}")
        print("   Run data_preprocessing.py first")
        return
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Train resume classifier
    print("\n2️⃣  Training resume category classifier...")
    model_results = trainer.train_resume_category_classifier(training_data)
    
    # Train skill extractor
    print("\n3️⃣  Training skill extraction model...")
    skill_results = trainer.train_skill_extractor(training_data)
    
    # Evaluate
    print("\n4️⃣  Evaluating models...")
    trainer.evaluate_models(model_results)
    
    # Save report
    print("\n5️⃣  Saving training report...")
    trainer.save_training_report(training_data, model_results, skill_results)
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\nModels saved in 'models/' directory:")
    for file in os.listdir(trainer.model_dir):
        print(f"  - {file}")


if __name__ == "__main__":
    main()
