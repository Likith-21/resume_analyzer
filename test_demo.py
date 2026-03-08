"""
Demo Script - Test all modules without Streamlit
Run this to verify everything is working correctly
"""

import sys
from pathlib import Path

# Add paths
sys.path.append(str(Path(__file__).parent / 'modules'))
sys.path.append(str(Path(__file__).parent / 'data'))

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.job_matcher import JobMatcher
import pandas as pd


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def test_skill_extractor():
    """Test skill extraction"""
    print_header("Testing Skill Extractor")
    
    sample_text = """
    I am a Data Scientist with 4 years of experience in Python, Machine Learning, and Deep Learning.
    I am proficient in TensorFlow, PyTorch, and Scikit-learn.
    I have experience with SQL, PostgreSQL, and MongoDB.
    I am skilled in AWS, Docker, and Kubernetes for deployment.
    I also know NLP and Computer Vision using Transformers and BERT.
    """
    
    try:
        skill_extractor = SkillExtractor()
        
        # Extract skills
        skills = skill_extractor.extract_skills(sample_text)
        print(f"✅ Skills Extracted: {len(skills)} found")
        print(f"   Skills: {', '.join(skills[:10])}")
        
        # Extract by category
        skills_cat = skill_extractor.extract_skills_by_category(sample_text)
        print(f"\n✅ Skills by Category:")
        for cat, cat_skills in skills_cat.items():
            print(f"   {cat}: {', '.join(cat_skills[:3])}")
        
        # Education
        education = skill_extractor.extract_education(sample_text)
        print(f"\n✅ Education: {education}")
        
        # Experience
        exp = skill_extractor.estimate_experience_years(sample_text)
        print(f"✅ Experience: {exp} years")
        
        # Score
        score = skill_extractor.get_skill_score(skills)
        print(f"✅ Skill Score: {score:.2f}/100")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_job_matcher():
    """Test job matching"""
    print_header("Testing Job Matcher")
    
    sample_resume = """
    Data Scientist with expertise in Python, Machine Learning, Deep Learning, TensorFlow, 
    Data Analysis, SQL, Pandas, NumPy, and AWS cloud platform. 4 years of professional experience.
    """
    
    try:
        # Load jobs
        jobs_path = Path(__file__).parent / 'data' / 'jobs.csv'
        jobs_df = pd.read_csv(jobs_path)
        print(f"✅ Loaded {len(jobs_df)} jobs from CSV")
        
        # Create matcher
        matcher = JobMatcher(jobs_df)
        
        # Extract skills for matching
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills(sample_resume)
        
        # Get recommendations
        recommendations = matcher.get_top_recommendations(
            sample_resume, 
            skills, 
            top_n=5
        )
        
        print(f"\n✅ Top 5 Job Recommendations:")
        for idx, job in enumerate(recommendations, 1):
            print(f"\n   {idx}. {job['job_title']} at {job['company']}")
            print(f"      Match Score: {job['combined_score']:.1f}%")
            print(f"      Skill Match: {job['skill_match']:.1f}%")
            print(f"      Content Match: {job['similarity_score']:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_skill_gap():
    """Test skill gap analysis"""
    print_header("Testing Skill Gap Analysis")
    
    sample_resume = """
    Experienced Python developer with Machine Learning and Deep Learning expertise.
    Skills: Python, Machine Learning, TensorFlow, Data Analysis, SQL
    """
    
    try:
        # Setup
        jobs_path = Path(__file__).parent / 'data' / 'jobs.csv'
        jobs_df = pd.read_csv(jobs_path)
        matcher = JobMatcher(jobs_df)
        skill_extractor = SkillExtractor()
        
        skills = skill_extractor.extract_skills(sample_resume)
        
        # Analyze gap for first job
        job_title = jobs_df.iloc[0]['job_title']
        gap_analysis = matcher.analyze_skill_gap(skills, job_title)
        
        print(f"✅ Analyzing gap for: {job_title}")
        print(f"   You have: {len(gap_analysis['matching_skills'])} skills")
        print(f"   You need: {len(gap_analysis['missing_skills'])} skills")
        print(f"   Match: {gap_analysis['skill_match_percentage']:.1f}%")
        
        if gap_analysis['matching_skills']:
            print(f"\n   Your Skills: {', '.join(gap_analysis['matching_skills'][:3])}")
        
        if gap_analysis['missing_skills']:
            print(f"   Learn These: {', '.join(gap_analysis['missing_skills'][:3])}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_resume_parser():
    """Test resume parser"""
    print_header("Testing Resume Parser")
    
    sample_text = """
    John Smith
    Email: john.smith@email.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johnsmith
    GitHub: github.com/johnsmith
    
    Senior Data Scientist with B.Tech and M.Tech degrees.
    """
    
    try:
        # Extract email
        email = ResumeParser.extract_email(sample_text)
        print(f"✅ Email extracted: {email}")
        
        # Extract phone
        phone = ResumeParser.extract_phone(sample_text)
        print(f"✅ Phone extracted: {phone}")
        
        # Extract URLs
        urls = ResumeParser.extract_urls(sample_text)
        print(f"✅ URLs extracted: {len(urls)} found")
        
        # Clean text
        clean = ResumeParser.clean_text(sample_text)
        print(f"✅ Text cleaned: {len(clean)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_data_files():
    """Test data files"""
    print_header("Testing Data Files")
    
    try:
        # Check skills database
        from data.skills_database import get_all_skills, TECHNICAL_SKILLS
        all_skills = get_all_skills()
        print(f"✅ Skills Database: {len(all_skills)} skills loaded")
        print(f"   Categories: {len(TECHNICAL_SKILLS)}")
        
        # Check jobs CSV
        jobs_path = Path(__file__).parent / 'data' / 'jobs.csv'
        jobs_df = pd.read_csv(jobs_path)
        print(f"\n✅ Jobs CSV: {len(jobs_df)} jobs loaded")
        print(f"   Columns: {', '.join(jobs_df.columns.tolist())}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🧪 AI RESUME SCREENING SYSTEM - DEMO & TEST".center(60))
    print("Testing all modules and functionality\n")
    
    results = {}
    
    # Run tests
    results['Data Files'] = test_data_files()
    results['Resume Parser'] = test_resume_parser()
    results['Skill Extractor'] = test_skill_extractor()
    results['Job Matcher'] = test_job_matcher()
    results['Skill Gap Analysis'] = test_skill_gap()
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ All tests passed! System is ready.")
        print("\nRun the web app with:")
        print("  streamlit run app.py")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
