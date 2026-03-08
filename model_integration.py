"""
Model Integration Layer
Loads trained models and integrates them with the application
"""

import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path


class ModelManager:
    """Manages loading and using trained ML models"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.classifier = None
        self.classifier_vectorizer = None
        self.skill_models = None
        self.skill_vectorizer = None
        self.is_trained = False
        
        self.load_models()
    
    def load_models(self):
        """Load all trained models from disk"""
        print("🔄 Loading trained models...")
        
        classifier_path = os.path.join(self.model_dir, 'resume_category_classifier.pkl')
        vectorizer_path = os.path.join(self.model_dir, 'resume_category_classifier_vectorizer.pkl')
        
        skill_models_path = os.path.join(self.model_dir, 'skill_extractor_model_models.pkl')
        skill_vectorizer_path = os.path.join(self.model_dir, 'skill_extractor_model_vectorizer.pkl')
        
        # Load classifier
        if os.path.exists(classifier_path) and os.path.exists(vectorizer_path):
            try:
                self.classifier = joblib.load(classifier_path)
                self.classifier_vectorizer = joblib.load(vectorizer_path)
                print("✅ Resume classifier loaded")
                self.is_trained = True
            except Exception as e:
                print(f"⚠️  Error loading classifier: {e}")
        
        # Load skill models
        if os.path.exists(skill_models_path) and os.path.exists(skill_vectorizer_path):
            try:
                self.skill_models = joblib.load(skill_models_path)
                self.skill_vectorizer = joblib.load(skill_vectorizer_path)
                print("✅ Skill extractor models loaded")
                self.is_trained = True
            except Exception as e:
                print(f"⚠️  Error loading skill models: {e}")
        
        if not self.is_trained:
            print("⚠️  No trained models found. Using rule-based matching.")
            print("   To train models: python complete_workflow.py")
    
    def predict_category(self, resume_text):
        """Predict resume category using trained classifier"""
        if not self.classifier or not self.classifier_vectorizer:
            return None
        
        try:
            # Vectorize
            X = self.classifier_vectorizer.transform([resume_text])
            
            # Predict
            prediction = self.classifier.predict(X)[0]
            confidence = np.max(self.classifier.predict_proba(X))
            
            return {
                'category': prediction,
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error predicting category: {e}")
            return None
    
    def predict_skills(self, resume_text):
        """Predict skills using trained models"""
        if not self.skill_models or not self.skill_vectorizer:
            return None
        
        try:
            results = {}
            X = self.skill_vectorizer.transform([resume_text])
            
            for skill, model_info in self.skill_models.items():
                model = model_info['model']
                prob = model.predict_proba(X)[0][1]
                
                if prob > 0.5:  # Confidence threshold
                    results[skill] = round(prob * 100, 2)
            
            return results
        except Exception as e:
            print(f"Error predicting skills: {e}")
            return None
    
    def enhance_job_matching(self, resume_text, jobs_df, job_matcher):
        """Enhance job recommendations using trained models"""
        recommendations = []
        
        # Get category prediction
        category_pred = self.predict_category(resume_text)
        if category_pred:
            print(f"\n🎯 Detected Category: {category_pred['category']} ({category_pred['confidence']:.1%})")
        
        # Get skill predictions
        skill_pred = self.predict_skills(resume_text)
        if skill_pred:
            print(f"\n🔧 Predicted Skills: {', '.join(list(skill_pred.keys())[:5])}")
        
        # Use existing job_matcher for recommendations
        if hasattr(job_matcher, 'get_top_recommendations'):
            top_jobs = job_matcher.get_top_recommendations(
                resume_text, 
                jobs_df, 
                top_n=10
            )
            
            # Potentially weight by category match
            if category_pred:
                for job in top_jobs:
                    # Boost score if job category matches predicted category
                    if category_pred['category'].lower() in str(job.get('job_title', '')).lower():
                        job['ml_confidence'] = category_pred['confidence']
            
            return top_jobs
        
        return []
    
    def get_model_stats(self):
        """Get statistics about loaded models"""
        stats = {
            'classifier_loaded': self.classifier is not None,
            'skill_models_loaded': self.skill_models is not None,
            'is_trained': self.is_trained
        }
        
        if self.skill_models:
            stats['num_skill_models'] = len(self.skill_models)
        
        return stats


class EnsemblePredictor:
    """Combines rule-based and ML-based predictions"""
    
    def __init__(self, job_matcher, model_manager):
        self.job_matcher = job_matcher
        self.model_manager = model_manager
        self.use_ml = model_manager.is_trained
    
    def predict_top_jobs(self, resume_text, jobs_df, top_n=10):
        """
        Predict top matching jobs using ensemble approach
        Combines rule-based job_matcher with ML predictions
        """
        
        # Method 1: Rule-based matching (always available)
        rule_based_jobs = self.job_matcher.get_top_recommendations(
            resume_text, 
            jobs_df, 
            top_n=top_n*2  # Get more for filtering
        )
        
        # Method 2: ML-based enhancement (if models are trained)
        if self.use_ml:
            ml_skills = self.model_manager.predict_skills(resume_text)
            category_pred = self.model_manager.predict_category(resume_text)
            
            # Score boost for jobs matching predicted category
            for job in rule_based_jobs:
                job['ml_score'] = 0.0
                
                if category_pred:
                    job_title_lower = str(job.get('job_title', '')).lower()
                    category_lower = category_pred['category'].lower()
                    
                    if category_lower in job_title_lower:
                        job['ml_score'] += 20  # Category match bonus
                
                if ml_skills:
                    job_desc = str(job.get('job_description', '')).lower()
                    skill_match_count = 0
                    for skill in ml_skills.keys():
                        if skill.lower() in job_desc:
                            skill_match_count += 1
                    
                    job['ml_score'] += (skill_match_count * 5)  # Skill match bonus
                
                # Combine scores
                original_score = job.get('match_percentage', 0)
                job['combined_score'] = (original_score * 0.6) + (job['ml_score'] * 0.4)
            
            # Sort by combined score
            rule_based_jobs.sort(key=lambda x: x.get('combined_score', 0), reverse=True)
        
        # Return top N
        return rule_based_jobs[:top_n]
    
    def get_skill_gap(self, resume_text, target_job_desc, all_skills_db):
        """
        Analyze skill gap between resume and target job
        Enhanced with ML predictions
        """
        
        # Traditional gap analysis
        gap = self.job_matcher.analyze_skill_gap(
            resume_text, 
            target_job_desc, 
            all_skills_db
        )
        
        # ML enhancement
        if self.use_ml:
            ml_predictions = self.model_manager.predict_skills(resume_text)
            
            if ml_predictions and 'gap' in gap:
                ml_missing = []
                for skill in gap['gap']:
                    if skill not in ml_predictions:
                        ml_missing.append(skill)
                
                gap['ml_confirmed_gap'] = ml_missing
        
        return gap


# Convenience function for Streamlit app
def get_model_manager():
    """Factory function to get model manager instance"""
    return ModelManager()


def get_ensemble_predictor(job_matcher):
    """Factory function to get ensemble predictor"""
    model_manager = ModelManager()
    return EnsemblePredictor(job_matcher, model_manager)
