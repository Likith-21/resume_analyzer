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
        
        # Pre-compile regex pattern for all skills (sorted by length, longest first)
        sorted_skills = sorted(self.all_skills, key=len, reverse=True)
        skill_pattern = '|'.join(re.escape(skill) for skill in sorted_skills)
        self.compiled_pattern = re.compile(r'\b(' + skill_pattern + r')\b', re.IGNORECASE)
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text (OPTIMIZED)
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            List of detected skills
        """
        # Find all skill matches using pre-compiled regex pattern
        matches = self.compiled_pattern.findall(resume_text)
        
        if not matches:
            return []
        
        # Create a mapping of lowercase skill names to original case
        skill_map = {skill.lower(): skill for skill in self.all_skills}
        
        # Return unique skills in original case
        detected_skills = []
        seen = set()
        for match in matches:
            match_lower = match.lower()
            if match_lower not in seen:
                # Get the original skill name from database
                original_skill = skill_map.get(match_lower, match)
                detected_skills.append(original_skill)
                seen.add(match_lower)
        
        return detected_skills
    
    def extract_skills_by_category(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract skills grouped by category (OPTIMIZED)
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dictionary with skills grouped by category
        """
        # Get detected skills first
        detected_skills = self.extract_skills(resume_text)
        detected_set = {skill.lower() for skill in detected_skills}
        
        # Create a skill to category mapping for faster lookup
        skill_to_category = {}
        for category, skills in self.technical_skills.items():
            for skill in skills:
                skill_lower = skill.lower()
                if skill_lower not in skill_to_category:
                    skill_to_category[skill_lower] = category
        
        # Group detected skills by category
        skills_by_category = {}
        for skill in detected_skills:
            skill_lower = skill.lower()
            category = skill_to_category.get(skill_lower)
            if category:
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill)
        
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
