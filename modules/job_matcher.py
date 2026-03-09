"""
Job Matcher Module
Matches resume with job descriptions using similarity algorithms
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import numpy as np


class JobMatcher:
    """Matches resumes with job descriptions"""
    
    def __init__(self, jobs_df: pd.DataFrame):
        """
        Initialize job matcher
        
        Args:
            jobs_df: DataFrame containing job descriptions
        """
        self.jobs_df = jobs_df
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', max_features=1000)
        
        # Pre-vectorize all job descriptions on initialization
        self.job_descriptions_vector = self.vectorizer.fit_transform(
            self.jobs_df['job_description'].fillna('')
        )
    
    def prepare_job_descriptions(self):
        """Job descriptions already vectorized in __init__"""
        pass
    
    def calculate_similarity(self, resume_text: str) -> List[Tuple[int, str, str, float]]:
        """
        Calculate similarity between resume and job descriptions
        
        Args:
            resume_text: Resume text
            
        Returns:
            List of tuples (job_id, job_title, company, similarity_score)
        """
        # Vectorize resume
        resume_vector = self.vectorizer.transform([resume_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(resume_vector, self.job_descriptions_vector)[0]
        
        # Create results
        results = []
        for idx, similarity_score in enumerate(similarities):
            job_id = self.jobs_df.iloc[idx]['job_id']
            job_title = self.jobs_df.iloc[idx]['job_title']
            company = self.jobs_df.iloc[idx]['company']
            
            # Convert to percentage
            percentage_score = similarity_score * 100
            
            results.append((job_id, job_title, company, percentage_score))
        
        return results
    
    def match_by_skills(self, resume_skills: List[str]) -> List[Dict]:
        """
        Match jobs based on required skills
        
        Args:
            resume_skills: List of skills extracted from resume
            
        Returns:
            List of matching jobs with skill match scores
        """
        results = []
        resume_skills_lower = [s.lower() for s in resume_skills]
        
        for idx, row in self.jobs_df.iterrows():
            job_skills = str(row['required_skills']).lower().split(', ')
            
            # Calculate skill match
            matching_skills = [skill for skill in job_skills if skill in resume_skills_lower]
            match_percentage = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
            
            results.append({
                'job_id': row['job_id'],
                'job_title': row['job_title'],
                'company': row['company'],
                'skill_match': match_percentage,
                'matching_skills': matching_skills,
                'missing_skills': [s for s in job_skills if s not in resume_skills_lower]
            })
        
        return results
    
    def get_top_recommendations(self, 
                                 resume_text: str, 
                                 resume_skills: List[str],
                                 top_n: int = 5) -> List[Dict]:
        """
        Get top job recommendations
        
        Args:
            resume_text: Resume text
            resume_skills: List of extracted skills
            top_n: Number of top recommendations to return
            
        Returns:
            List of top matching jobs with combined score
        """
        # Get similarity scores
        similarity_results = self.calculate_similarity(resume_text)
        
        # Get skill-based match
        skill_results = self.match_by_skills(resume_skills)
        
        # Create skill score dictionary
        skill_dict = {job['job_id']: job['skill_match'] for job in skill_results}
        
        # Combine scores (60% similarity + 40% skill match)
        combined_results = []
        for job_id, job_title, company, sim_score in similarity_results:
            skill_score = skill_dict.get(job_id, 0)
            combined_score = (sim_score * 0.6) + (skill_score * 0.4)
            
            # Get detailed info
            job_info = next((j for j in skill_results if j['job_id'] == job_id), {})
            
            combined_results.append({
                'job_id': job_id,
                'job_title': job_title,
                'company': company,
                'combined_score': combined_score,
                'similarity_score': sim_score,
                'skill_match': skill_score,
                'matching_skills': job_info.get('matching_skills', []),
                'missing_skills': job_info.get('missing_skills', []),
                'experience_required': self.jobs_df.iloc[job_id-1]['experience_years'],
                'location': self.jobs_df.iloc[job_id-1]['location'],
                'salary_range': self.jobs_df.iloc[job_id-1]['salary_range']
            })
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return combined_results[:top_n]
    
    def analyze_skill_gap(self, resume_skills: List[str], job_title: str) -> Dict:
        """
        Analyze skill gap for a specific job
        
        Args:
            resume_skills: List of extracted skills
            job_title: Job title to analyze
            
        Returns:
            Dictionary with skill gap analysis
        """
        # Find the job
        job = self.jobs_df[self.jobs_df['job_title'] == job_title]
        
        if job.empty:
            return {'error': 'Job not found'}
        
        job = job.iloc[0]
        required_skills = [s.strip() for s in job['required_skills'].split(',')]
        resume_skills_lower = [s.lower() for s in resume_skills]
        
        # Find matching and missing skills
        matching = [s for s in required_skills if s.lower() in resume_skills_lower]
        missing = [s for s in required_skills if s.lower() not in resume_skills_lower]
        
        return {
            'job_title': job_title,
            'company': job['company'],
            'total_required': len(required_skills),
            'matching_skills': matching,
            'missing_skills': missing,
            'skill_match_percentage': (len(matching) / len(required_skills)) * 100 if required_skills else 0,
            'experience_required': job['experience_years']
        }
