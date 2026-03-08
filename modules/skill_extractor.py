"""
Skill Extractor Module
Extracts skills from resume text
"""

import re
from typing import List, Dict
import sys
sys.path.append('../data')

from data.skills_database import get_all_skills, TECHNICAL_SKILLS


class SkillExtractor:
    """Extracts technical skills from resume text"""
    
    def __init__(self):
        """Initialize skill extractor with skill database"""
        self.all_skills = get_all_skills()
        self.technical_skills = TECHNICAL_SKILLS
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            List of detected skills
        """
        resume_lower = resume_text.lower()
        detected_skills = []
        
        # Search for each skill in the resume
        for skill in self.all_skills:
            skill_lower = skill.lower()
            
            # Use word boundary matching to avoid partial matches
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_lower):
                if skill not in detected_skills:
                    detected_skills.append(skill)
        
        return detected_skills
    
    def extract_skills_by_category(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract skills grouped by category
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dictionary with skills grouped by category
        """
        resume_lower = resume_text.lower()
        skills_by_category = {}
        
        for category, skills in self.technical_skills.items():
            category_skills = []
            for skill in skills:
                skill_lower = skill.lower()
                if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_lower):
                    category_skills.append(skill)
            
            if category_skills:
                skills_by_category[category] = category_skills
        
        return skills_by_category
    
    def extract_education(self, resume_text: str) -> List[str]:
        """
        Extract education details from resume
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            List of education details
        """
        degrees = ['B.Tech', 'B.S', 'B.Sc', 'M.Tech', 'M.S', 'M.Sc', 
                   'MBA', 'Ph.D', 'PhD', 'BE', 'ME', 'BCA', 'MCA',
                   'Bachelor', 'Master', 'Doctorate']
        
        education_list = []
        resume_lower = resume_text.lower()
        
        for degree in degrees:
            if degree.lower() in resume_lower:
                education_list.append(degree)
        
        return list(set(education_list))  # Remove duplicates
    
    def estimate_experience_years(self, resume_text: str) -> int:
        """
        Estimate years of experience from resume
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Estimated years of experience
        """
        # Look for year patterns like "2020-2023", "2+ years", "5 years"
        patterns = [
            r'(\d{1,2})\s*(?:\+)?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d{4})\s*[-–]\s*(?:present|now|current|ongoing)',
            r'experience\s*(?:since|from)?\s*(\d{4})',
        ]
        
        years_found = []
        
        for pattern in patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                try:
                    year_or_exp = int(match)
                    if year_or_exp > 1900:  # It's a year
                        years_found.append(2024 - year_or_exp)
                    else:  # It's years of experience
                        years_found.append(year_or_exp)
                except:
                    pass
        
        return max(years_found) if years_found else 0
    
    def get_skill_score(self, detected_skills: List[str]) -> float:
        """
        Calculate a score based on detected skills
        
        Args:
            detected_skills: List of detected skills
            
        Returns:
            Score out of 100
        """
        if not detected_skills:
            return 0.0
        
        # Weight different categories
        weights = {
            'programming_languages': 2.0,
            'machine_learning': 3.0,
            'data_science': 3.0,
            'cloud_platforms': 2.5,
            'database': 2.0,
            'devops': 2.0,
            'web_technologies': 1.5,
            'big_data': 2.5,
            'soft_skills': 1.0
        }
        
        total_score = 0.0
        
        for skill in detected_skills:
            for category, skill_list in self.technical_skills.items():
                if skill in skill_list:
                    total_score += weights.get(category, 1.0)
                    break
        
        # Normalize to 100
        max_possible_score = sum(weights.values()) * 2.5
        score = (total_score / max_possible_score) * 100
        
        return min(score, 100.0)  # Cap at 100
