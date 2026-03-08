# Project Configuration

PROJECT_NAME = "AI Resume Screening & Job Recommendation System"
VERSION = "1.0.0"
AUTHOR = "Your Name"

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['pdf', 'docx']
UPLOAD_FOLDER = 'uploads'

# Matching Algorithm Configuration
SIMILARITY_WEIGHT = 0.6  # Weight for TF-IDF similarity
SKILL_MATCH_WEIGHT = 0.4  # Weight for skill matching

# Top Recommendations
TOP_RECOMMENDATIONS = 10

# Skill Categories for Display
SKILL_CATEGORIES = [
    'programming_languages',
    'web_technologies',
    'database',
    'machine_learning',
    'data_science',
    'cloud_platforms',
    'big_data',
    'devops'
]
