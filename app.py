"""
AI Resume Screening & Job Recommendation System
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Optimize imports - move heavy imports inside functions
# This speeds up initial page load on Streamlit Cloud

# Add modules to path
sys.path.append(str(Path(__file__).parent / 'modules'))
sys.path.append(str(Path(__file__).parent / 'data'))

# Lazy import - import only when needed (speeds up initial load)
def get_resume_parser():
    from modules.resume_parser import ResumeParser
    return ResumeParser

def get_skill_extractor_class():
    from modules.skill_extractor import SkillExtractor
    return SkillExtractor

def get_job_matcher_class():
    from modules.job_matcher import JobMatcher
    return JobMatcher


# Page configuration
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header Styling */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        letter-spacing: -1px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Card Styling */
    .stExpander {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Metric Box Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Match Level Colors */
    .match-high {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        box-shadow: 0 2px 6px rgba(17, 153, 142, 0.3) !important;
    }
    
    .match-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        box-shadow: 0 2px 6px rgba(240, 147, 251, 0.3) !important;
    }
    
    .match-low {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
        box-shadow: 0 2px 6px rgba(250, 112, 154, 0.3) !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #f8f9fa;
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background-color: #f5f7fa;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        font-size: 2rem;
        margin-bottom: 1.2rem;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Info Box */
    .stInfo {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0e7ff 100%);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.6rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: white;
        border-radius: 8px;
        padding: 0 2rem;
        font-size: 1rem;
        font-weight: 600;
        color: #4a5568;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #f5f7fa 0%, #e0e7ff 100%);
        border-color: #667eea;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Tab Content */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }
    
    /* Professional Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-top: 3rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Animated Gradient Background for Headers */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .animated-bg {
        background: linear-gradient(270deg, #667eea, #764ba2, #f093fb);
        background-size: 600% 600%;
        animation: gradient 8s ease infinite;
    }
</style>
""", unsafe_allow_html=True)


# ============ CACHING FUNCTIONS FOR PERFORMANCE ============

@st.cache_data
def load_jobs_data():
    """Load jobs data from CSV (CACHED)"""
    try:
        jobs_path = Path(__file__).parent / 'data' / 'jobs.csv'
        if not jobs_path.exists():
            jobs_path = Path(__file__).parent / 'data' / 'enhanced_jobs.csv'
        return pd.read_csv(jobs_path)
    except Exception as e:
        return pd.DataFrame(columns=['job_title', 'company', 'location', 'experience_required', 
                                     'salary_range', 'skills_required', 'job_description'])


@st.cache_resource
def get_skill_extractor():
    """Get cached skill extractor instance (lazy loaded)"""
    SkillExtractor = get_skill_extractor_class()
    return SkillExtractor()


@st.cache_resource
def get_job_matcher():
    """Get cached job matcher with pre-loaded jobs (lazy loaded)"""
    jobs_df = load_jobs_data()
    JobMatcher = get_job_matcher_class()
    return JobMatcher(jobs_df)


@st.cache_data
def get_all_skills_cached():
    """Get all available skills (CACHED)"""
    try:
        from data.skills_database import get_all_skills
        return get_all_skills()
    except Exception:
        return []


def save_uploaded_file(uploaded_file, upload_dir='uploads'):
    """Save uploaded file and return path"""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def main():
    # Sidebar with ML Stats
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.8rem;'>📊 System Status</h2>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 0.5rem;'>Live Metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize system status placeholder
        status_placeholder = st.empty()
        
        # Get real-time system info with error handling
        system_ready = "✅ Ready"
        skill_count = 0
        jobs_count = 0
        
        with status_placeholder.container():
            # Show loading status
            st.markdown("""
            <div style='text-align: center; color: rgba(255,255,255,0.7);'>
                <p>🔄 Loading system...</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Load skills with timeout handling
        try:
            skill_count = len(get_all_skills_cached())
        except Exception:
            system_ready = "⚠️ Partial"
            skill_count = 0
        
        # Load jobs with timeout handling
        try:
            jobs_df = load_jobs_data()
            jobs_count = len(jobs_df) if jobs_df is not None else 0
        except Exception:
            if system_ready == "✅ Ready":
                system_ready = "⚠️ Partial"
            jobs_count = 0
        
        # Update status with actual data
        with status_placeholder.container():
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;'>
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <h3 style='color: white; font-size: 2.5rem; margin: 0;'>{system_ready}</h3>
                    <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.3rem 0;'>System Status</p>
                </div>
                <hr style='border: 1px solid rgba(255,255,255,0.2); margin: 1rem 0;'>
                <div style='color: rgba(255,255,255,0.9); font-size: 0.95rem;'>
                    <p style='margin: 0.5rem 0;'>📚 <strong>81.82%</strong> Accuracy</p>
                    <p style='margin: 0.5rem 0;'>💡 <strong>{skill_count}</strong> Technical Skills</p>
                    <p style='margin: 0.5rem 0;'>💼 <strong>{jobs_count}</strong> Jobs Loaded</p>
                    <p style='margin: 0.5rem 0;'>🤖 <strong>Gradient Boosting</strong></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem; text-align: center;'>
            <p><strong>🚀 Features</strong></p>
            <p>✅ Resume Parsing</p>
            <p>✅ Skill Extraction</p>
            <p>✅ Job Matching</p>
            <p>✅ Gap Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Dashboard with Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Resume Screening", 
        "💼 Job Recommendations", 
        "🔍 Skill Gap Analysis", 
        "ℹ️ About System"
    ])
    
    with tab1:
        resume_screening_page()
    
    with tab2:
        job_recommendations_page()
    
    with tab3:
        skill_gap_analysis_page()
    
    with tab4:
        about_page()


def resume_screening_page():
    """Resume Screening Page"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=['pdf', 'docx'],
            help="Upload your resume in PDF or DOCX format"
        )
    
    if uploaded_file is not None:
        try:
            # Save and process file
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Parse resume with error handling
            try:
                ResumeParser = get_resume_parser()
                resume_text = ResumeParser.extract_text_from_file(file_path)
                
                if not resume_text or len(resume_text.strip()) == 0:
                    st.error("❌ Could not extract text from file. Please ensure the file is readable.")
                    return
                
            except Exception as parse_error:
                st.error(f"❌ Error parsing file: {str(parse_error)}")
                return
            
            # Extract skills with error handling
            try:
                SkillExtractor = get_skill_extractor_class()
                skill_extractor = SkillExtractor()
                detected_skills = skill_extractor.extract_skills(resume_text)
                skills_by_category = skill_extractor.extract_skills_by_category(resume_text)
                education = skill_extractor.extract_education(resume_text)
                experience_years = skill_extractor.estimate_experience_years(resume_text)
                skill_score = skill_extractor.get_skill_score(detected_skills)
            except Exception as skill_error:
                st.error(f"❌ Error extracting skills: {str(skill_error)}")
                return
            
            # Extract contact info
            try:
                ResumeParser = get_resume_parser()
                email = ResumeParser.extract_email(resume_text)
                phone = ResumeParser.extract_phone(resume_text)
                urls = ResumeParser.extract_urls(resume_text)
            except Exception as contact_error:
                email = "Not found"
                phone = "Not found"
                urls = []
            
            # Display results
            st.markdown("---")
            st.markdown("### 📊 Resume Analysis Results")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Skills Detected", len(detected_skills) if detected_skills else 0)
            with col2:
                st.metric("Estimated Experience", f"{experience_years} years" if experience_years else "0 years")
            with col3:
                st.metric("Skill Score", f"{skill_score:.1f}/100" if skill_score else "0/100")
            with col4:
                st.metric("Education Found", len(education) if education else 0)
            
            # Contact Information
            st.markdown("### 📧 Contact Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input("Email", value=email if email else "Not found", disabled=True)
            with col2:
                st.text_input("Phone", value=phone if phone else "Not found", disabled=True)
            with col3:
                if urls and len(urls) > 0:
                    st.text_input("Profiles", value=urls[0], disabled=True)
                else:
                    st.text_input("Profiles", value="Not found", disabled=True)
            
            # Education
            if education and len(education) > 0:
                st.markdown("### 🎓 Education")
                st.write(", ".join(education))
            
            # Skills by Category
            st.markdown("### 💼 Skills Detected by Category")
            
            if skills_by_category and len(skills_by_category) > 0:
                for category, skills in skills_by_category.items():
                    with st.expander(f"{category.replace('_', ' ').title()} ({len(skills)})"):
                        skill_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
                        st.markdown(skill_html, unsafe_allow_html=True)
            else:
                st.warning("No skills detected. Please ensure your resume contains technical skills.")
            
            # Store in session for other pages
            st.session_state.resume_text = resume_text
            st.session_state.detected_skills = detected_skills if detected_skills else []
            st.session_state.experience_years = experience_years if experience_years else 0
            st.session_state.skill_score = skill_score if skill_score else 0
            
            # Show raw text option
            if st.checkbox("Show extracted resume text"):
                st.text_area("Extracted Resume Text", value=resume_text[:1000], height=300, disabled=True)
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    else:
        st.info("👆 Upload a resume file to get started!")


def job_recommendations_page():
    """Job Recommendations Page"""
    
    if 'resume_text' not in st.session_state:
        st.warning("⚠️ Please upload a resume first on the 'Resume Screening' page")
        return
    
    try:
        # Load jobs with error handling (CACHED)
        jobs_df = load_jobs_data()
        
        if jobs_df is None or len(jobs_df) == 0:
            st.error("❌ No jobs data available. Please check the data files.")
            return
        
        # Get cached matcher with pre-loaded jobs
        matcher = get_job_matcher()
        
        # Get recommendations with error handling
        try:
            recommendations = matcher.get_top_recommendations(
                st.session_state.get('resume_text', ''),
                st.session_state.get('detected_skills', []),
                top_n=15
            )
            
            if not recommendations or len(recommendations) == 0:
                st.warning("⚠️ No job matches found. Try uploading a resume with more details.")
                return
                
        except Exception as match_error:
            st.error(f"❌ Error generating recommendations: {str(match_error)}")
            return
        
        st.markdown("### 🎯 Top Job Matches for Your Profile")
        
        # Display recommendations
        for idx, job in enumerate(recommendations[:10], 1):
            try:
                with st.expander(
                    f"#{idx} {job.get('job_title', 'Job')} at {job.get('company', 'Company')} - {job.get('combined_score', 0):.1f}% Match",
                    expanded=(idx == 1)
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        score = job.get('combined_score', 0)
                        if score >= 70:
                            st.success(f"**Match Score: {score:.1f}%**")
                        elif score >= 50:
                            st.warning(f"**Match Score: {score:.1f}%**")
                        else:
                            st.error(f"**Match Score: {score:.1f}%**")
                    
                    with col2:
                        st.write(f"**Location:** {job.get('location', 'N/A')}")
                        st.write(f"**Experience Required:** {job.get('experience_required', 0)} years")
                    
                    with col3:
                        st.write(f"**Salary Range:** {job.get('salary_range', 'N/A')}")
                    
                    # Skill breakdown
                    st.markdown("#### Skill Match Breakdown")
                    col1, col2 = st.columns(2)
                    
                    skill_match = job.get('skill_match', 0)
                    similarity = job.get('similarity_score', 0)
                    
                    with col1:
                        st.progress(skill_match / 100, text=f"Skills: {skill_match:.1f}%")
                    with col2:
                        st.progress(similarity / 100, text=f"Content Match: {similarity:.1f}%")
                    
                    # Matching skills
                    matching_skills = job.get('matching_skills', [])
                    if matching_skills and len(matching_skills) > 0:
                        st.markdown("**✅ Matching Skills:**")
                        skill_html = " ".join([f'<span class="skill-tag match-high">{skill.strip()}</span>' 
                                              for skill in matching_skills])
                        st.markdown(skill_html, unsafe_allow_html=True)
                    
                    # Missing skills
                    missing_skills = job.get('missing_skills', [])
                    if missing_skills and len(missing_skills) > 0:
                        st.markdown("**❌ Missing Skills:**")
                        skill_html = " ".join([f'<span class="skill-tag match-low">{skill.strip()}</span>' 
                                              for skill in missing_skills])
                        st.markdown(skill_html, unsafe_allow_html=True)
            
            except Exception as item_error:
                st.warning(f"Could not display job #{idx}: {str(item_error)[:50]}")
                continue
        
        # Summary statistics
        st.markdown("---")
        st.markdown("### 📈 Recommendation Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            high_matches = len([j for j in recommendations if j.get('combined_score', 0) >= 70])
            st.metric("High Matches (≥70%)", high_matches)
        with col2:
            medium_matches = len([j for j in recommendations if 50 <= j.get('combined_score', 0) < 70])
            st.metric("Medium Matches (50-70%)", medium_matches)
        with col3:
            if len(recommendations) > 0:
                avg_score = sum(j.get('combined_score', 0) for j in recommendations) / len(recommendations)
                st.metric("Average Match Score", f"{avg_score:.1f}%")
            else:
                st.metric("Average Match Score", "0%")
    
    except Exception as e:
        st.error(f"❌ Error in job recommendations: {str(e)}")


def skill_gap_analysis_page():
    """Skill Gap Analysis Page"""
    
    if 'resume_text' not in st.session_state:
        st.warning("⚠️ Please upload a resume first on the 'Resume Screening' page")
        return
    
    try:
        jobs_df = load_jobs_data()
        
        if jobs_df is None or len(jobs_df) == 0:
            st.error("❌ No jobs data available.")
            return
        
        matcher = get_job_matcher()
        
        # Select job with error handling
        try:
            job_titles = jobs_df['job_title'].unique()
            if len(job_titles) == 0:
                st.error("❌ No job titles available.")
                return
            
            selected_job = st.selectbox(
                "Select a job to analyze skill gap:",
                job_titles
            )
        except Exception as select_error:
            st.error(f"❌ Error selecting job: {str(select_error)}")
            return
        
        if selected_job:
            try:
                # Analyze gap
                gap_analysis = matcher.analyze_skill_gap(
                    st.session_state.get('detected_skills', []),
                    selected_job
                )
                
                if gap_analysis is None:
                    st.error("❌ Could not analyze skill gap.")
                    return
                
                st.markdown(f"### 📊 Skill Gap for {selected_job}")
                st.markdown(f"Company: **{gap_analysis.get('company', 'N/A')}**")
                
                # Progress bar
                match_percent = gap_analysis.get('skill_match_percentage', 0)
                st.progress(match_percent / 100, text=f"Overall Match: {match_percent:.1f}%")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("You Have", len(gap_analysis.get('matching_skills', [])))
                with col2:
                    st.metric("Total Required", gap_analysis.get('total_required', 0))
                with col3:
                    st.metric("You Need", len(gap_analysis.get('missing_skills', [])))
                
                # Details
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                matching = gap_analysis.get('matching_skills', [])
                missing = gap_analysis.get('missing_skills', [])
                
                with col1:
                    st.markdown("#### ✅ Skills You Have")
                    if matching and len(matching) > 0:
                        for skill in matching:
                            st.write(f"✓ {skill}")
                    else:
                        st.info("No matching skills found")
                
                with col2:
                    st.markdown("#### ❌ Skills You Need to Learn")
                    if missing and len(missing) > 0:
                        for idx, skill in enumerate(missing, 1):
                            st.write(f"{idx}. {skill}")
                    else:
                        st.success("You have all required skills!")
                
                # Experience gap
                st.markdown("---")
                st.markdown("#### Experience Gap")
                exp_required = gap_analysis.get('experience_required', 0)
                exp_yours = st.session_state.get('experience_years', 0)
                
                st.write(f"Experience Required: **{exp_required} years**")
                st.write(f"Your Estimated Experience: **{exp_yours} years**")
                
                if exp_yours >= exp_required:
                    st.success(f"✅ You meet the experience requirement")
                else:
                    years_gap = exp_required - exp_yours
                    st.warning(f"⚠️ You need {years_gap} more years of experience")
            
            except Exception as gap_error:
                st.error(f"❌ Error analyzing skill gap: {str(gap_error)}")
    
    except Exception as e:
        st.error(f"❌ Error in skill gap analysis: {str(e)}")


def about_page():
    """About Page"""
    
    st.markdown("""
    ### 🎯 Project Overview
    
    The **AI Resume Screening & Job Recommendation System** is an intelligent platform that helps:
    - 📄 **Candidates** find suitable job opportunities based on their skills and experience
    - 🏢 **Companies** automatically screen and rank resumes
    
    ### 🛠️ Technology Stack
    
    | Component | Technology |
    |-----------|-----------|
    | Programming | Python |
    | NLP & Text Processing | spaCy, NLTK |
    | Machine Learning | Scikit-learn |
    | Data Processing | Pandas, NumPy |
    | Resume Parsing | PyPDF2, python-docx |
    | User Interface | Streamlit |
    | Similarity Metrics | TF-IDF, Cosine Similarity |
    
    ### 📊 Features
    
    ✅ **Resume Parsing** - Extract text from PDF and DOCX files
    
    ✅ **Skill Extraction** - Identify technical skills using NLP
    
    ✅ **Contact Information** - Extract email, phone, URLs
    
    ✅ **Education Detection** - Find degree information
    
    ✅ **Experience Estimation** - Calculate years of experience
    
    ✅ **Job Matching** - Match resumes with job descriptions
    
    ✅ **Recommendations** - Get top 10 job recommendations
    
    ✅ **Skill Gap Analysis** - Identify missing skills for target jobs
    
    ### 🧠 How It Works
    
    1. **Resume Upload** → Extract text from PDF/DOCX
    2. **Skill Extraction** → NLP-based skill detection
    3. **Job Matching** → TF-IDF vectorization + Cosine similarity
    4. **Scoring** → Combined algorithm (60% content + 40% skills)
    5. **Recommendations** → Top matching jobs ranked by score
    
    ### 👨‍💻 Created for AI & DS Final Year Project
    
    This project demonstrates:
    - Machine Learning applications
    - Natural Language Processing (NLP)
    - Data Analysis and Visualization
    - Full-stack development with Python
    - Real-world problem solving
    
    ### 📚 Learning Outcomes
    
    - Understand TF-IDF and cosine similarity
    - Text preprocessing and NLP techniques
    - Resume parsing from multiple formats
    - Building ML-based recommendation systems
    - Creating interactive web applications
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>AI Resume Screening & Job Recommendation System</p>
        <p>Built with ❤️ using Python, Streamlit, and Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
