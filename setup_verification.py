"""
Setup Verification Script
Checks if all dependencies and structure are in place before ML training
"""

import os
import sys
from pathlib import Path


class SetupVerifier:
    """Verify project setup for ML training"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        self.warnings = []
        self.successes = []
    
    # =====================================================================
    # VERIFICATION CHECKS
    # =====================================================================
    
    def check_python_version(self):
        """Verify Python version"""
        version = sys.version_info
        print(f"\n📌 Python Version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major >= 3 and version.minor >= 8:
            self.successes.append("Python version OK (3.8+)")
        else:
            self.issues.append("Python 3.8+ required")
    
    def check_required_packages(self):
        """Check if required packages are installed"""
        print("\n📦 Checking Required Packages:")
        
        required = {
            'pandas': 'Data manipulation',
            'numpy': 'Numerical computing',
            'sklearn': 'Machine Learning (scikit-learn)',
            'joblib': 'Model serialization',
            'streamlit': 'Web UI',
        }
        
        missing = []
        
        for package, description in required.items():
            try:
                import importlib
                if package == 'sklearn':
                    importlib.import_module('sklearn')
                else:
                    importlib.import_module(package)
                print(f"   ✅ {package}: {description}")
                self.successes.append(f"Package {package} installed")
            except ImportError:
                print(f"   ❌ {package}: {description} - MISSING")
                missing.append(package)
                self.issues.append(f"Missing package: {package}")
        
        if missing:
            print(f"\n   🔧 Install missing packages:")
            print(f"   pip install {' '.join(missing)}")
    
    def check_directory_structure(self):
        """Check if required directories exist"""
        print("\n📁 Checking Directory Structure:")
        
        required_dirs = [
            'data',
            'modules',
            'uploads'
        ]
        
        for dir_name in required_dirs:
            path = self.project_root / dir_name
            if path.exists():
                print(f"   ✅ {dir_name}/")
                self.successes.append(f"Directory {dir_name}/ exists")
            else:
                print(f"   ❌ {dir_name}/ - MISSING")
                self.issues.append(f"Missing directory: {dir_name}/")
    
    def check_data_files(self):
        """Check if data files exist"""
        print("\n📊 Checking Data Files:")
        
        required_files = {
            'data/jobs.csv': 'Job postings database',
            'data/resume_dataset.csv': 'Sample resume dataset',
            'data/skills_database.py': 'Skills database',
        }
        
        for file_path, description in required_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                size = os.path.getsize(full_path)
                print(f"   ✅ {file_path} ({size:,} bytes)")
                self.successes.append(f"File {file_path} exists")
            else:
                print(f"   ⚠️  {file_path} - NOT FOUND (needed for training)")
                self.warnings.append(f"Data file missing: {file_path}")
    
    def check_python_modules(self):
        """Check if project modules import correctly"""
        print("\n🔧 Checking Project Modules:")
        
        modules = {
            'modules.resume_parser': 'Resume text extraction',
            'modules.skill_extractor': 'Skill extraction',
            'modules.job_matcher': 'Job matching',
            'data.skills_database': 'Skills database',
        }
        
        for module, description in modules.items():
            try:
                import importlib
                importlib.import_module(module)
                print(f"   ✅ {module}: {description}")
                self.successes.append(f"Module {module} imports OK")
            except Exception as e:
                print(f"   ❌ {module}: {str(e)}")
                self.warnings.append(f"Module import issue: {module}")
    
    def check_ml_files(self):
        """Check if ML training files exist"""
        print("\n🤖 Checking ML Training Files:")
        
        ml_files = {
            'train_models.py': 'Model training',
            'complete_workflow.py': 'Complete workflow',
            'model_integration.py': 'Model integration',
            'quick_reference.py': 'Quick reference examples',
            'data_preprocessing.py': 'Data preprocessing',
        }
        
        for file_name, description in ml_files.items():
            full_path = self.project_root / file_name
            if file_name == 'data_preprocessing.py':
                full_path = self.project_root / 'data' / file_name
            
            if full_path.exists():
                lines = sum(1 for _ in open(full_path))
                print(f"   ✅ {file_name}: {description} ({lines} lines)")
                self.successes.append(f"File {file_name} exists")
            else:
                print(f"   ⚠️  {file_name}: {description} - NOT FOUND")
                self.warnings.append(f"ML file missing: {file_name}")
    
    def check_models_directory(self):
        """Check if models directory exists/has trained models"""
        print("\n🎯 Checking Models Directory:")
        
        models_dir = self.project_root / 'models'
        
        if models_dir.exists():
            files = list(models_dir.glob('*'))
            print(f"   ✅ models/ directory exists")
            
            if files:
                print(f"   ✅ Found {len(files)} trained model files")
                self.successes.append("Trained models found")
                for file in sorted(files):
                    print(f"      • {file.name}")
            else:
                print(f"   ℹ️  models/ directory is empty (no trained models yet)")
                self.warnings.append("No trained models yet - run training to create them")
        else:
            print(f"   ⚠️  models/ directory not found")
            print(f"       Will be created during training")
            self.warnings.append("Models directory will be created during training")
    
    def check_kaggle_data(self):
        """Check if Kaggle data directory exists"""
        print("\n🔍 Checking Kaggle Data:")
        
        kaggle_dir = self.project_root / 'data' / 'kaggle_datasets'
        
        if kaggle_dir.exists():
            files = list(kaggle_dir.glob('*'))
            print(f"   ✅ data/kaggle_datasets/ directory exists")
            
            if files:
                print(f"   ✅ Found {len(files)} Kaggle dataset files")
                self.successes.append(f"Kaggle data found ({len(files)} files)")
                for file in sorted(files[:5]):  # Show first 5
                    print(f"      • {file.name}")
                if len(files) > 5:
                    print(f"      ... and {len(files)-5} more")
            else:
                print(f"   ⚠️  data/kaggle_datasets/ directory is empty")
                print(f"       Download Kaggle datasets to proceed with training")
                self.warnings.append("Kaggle datasets not yet downloaded")
                print(f"\n       📋 See KAGGLE_DOWNLOAD_GUIDE.md for instructions")
        else:
            print(f"   ⚠️  data/kaggle_datasets/ directory not found (will create)")
            self.warnings.append("Kaggle data directory doesn't exist")
    
    def check_documentation(self):
        """Check if documentation files exist"""
        print("\n📖 Checking Documentation:")
        
        docs = {
            'ML_TRAINING_GUIDE.md': 'ML training guide',
            'ML_IMPLEMENTATION_SUMMARY.md': 'Implementation summary',
            'KAGGLE_DOWNLOAD_GUIDE.md': 'Kaggle download guide',
            'README.md': 'Project README',
        }
        
        for doc_name, description in docs.items():
            full_path = self.project_root / doc_name
            if full_path.exists():
                size = os.path.getsize(full_path)
                print(f"   ✅ {doc_name}")
                self.successes.append(f"Documentation {doc_name} found")
            else:
                print(f"   ✅ {doc_name}: Not found (not critical)")
    
    def check_gpu_availability(self):
        """Check if GPU is available"""
        print("\n⚡ Checking GPU Availability:")
        
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            
            if cuda_available:
                device_name = torch.cuda.get_device_name(0)
                print(f"   ✅ GPU Available: {device_name}")
                self.successes.append("GPU available for faster training")
            else:
                print(f"   ℹ️  GPU not available - will use CPU")
                print(f"       Training will be slower but still functional")
                self.warnings.append("GPU not available (training will be slower)")
        except ImportError:
            print(f"   ℹ️  PyTorch not installed")
            print(f"       GPU detection skipped (not required for basic training)")
    
    # =====================================================================
    # MAIN VERIFICATION FLOW
    # =====================================================================
    
    def run_all_checks(self):
        """Run all verification checks"""
        print("\n" + "="*70)
        print("  🔍 RESUME SCREENING SYSTEM - SETUP VERIFICATION")
        print("="*70)
        
        # Run all checks
        self.check_python_version()
        self.check_required_packages()
        self.check_directory_structure()
        self.check_data_files()
        self.check_python_modules()
        self.check_ml_files()
        self.check_models_directory()
        self.check_kaggle_data()
        self.check_documentation()
        self.check_gpu_availability()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print verification summary"""
        print("\n" + "="*70)
        print("  ✅ VERIFICATION SUMMARY")
        print("="*70)
        
        # Successes
        if self.successes:
            print(f"\n✅ PASSED ({len(self.successes)}):")
            for item in self.successes[:5]:  # Show first 5
                print(f"   • {item}")
            if len(self.successes) > 5:
                print(f"   ... and {len(self.successes)-5} more")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"   • {item}")
        
        # Critical Issues
        if self.issues:
            print(f"\n❌ ISSUES ({len(self.issues)}):")
            for item in self.issues:
                print(f"   • {item}")
        
        # Status
        print("\n" + "-"*70)
        if self.issues:
            print("❌ SETUP INCOMPLETE - Please fix critical issues above")
            print("\nNext Steps:")
            print("  1. Install missing packages (if any)")
            print("  2. Fix missing directories/files")
            print("  3. Download Kaggle datasets")
            print("  4. Run verification again")
            return False
        elif self.warnings:
            print("⚠️  SETUP READY WITH WARNINGS")
            print("\nYou can proceed, but note:")
            print("  • Kaggle data needs to be downloaded for full training")
            print("  • See ML_TRAINING_GUIDE.md for detailed instructions")
            print("\nNext Steps:")
            print("  1. Download Kaggle datasets (see KAGGLE_DOWNLOAD_GUIDE.md)")
            print("  2. Run: python complete_workflow.py")
            print("  3. Check: cat models/training_report.txt")
            return True
        else:
            print("✅ SETUP COMPLETE - Ready for ML training!")
            print("\nYou can now:")
            print("  1. Download Kaggle datasets (if not already done)")
            print("  2. Run: python complete_workflow.py")
            print("  3. Start web app: streamlit run app.py")
            return True
    
    def get_next_steps(self):
        """Return recommended next steps"""
        if self.issues:
            return [
                "Install missing Python packages",
                "Create missing directories",
                "Run setup verification again"
            ]
        elif self.warnings:
            return [
                "Download Kaggle datasets (KAGGLE_DOWNLOAD_GUIDE.md)",
                "Run: python complete_workflow.py",
                "Monitor training progress"
            ]
        else:
            return [
                "Optionally download Kaggle datasets for more training data",
                "Run: python complete_workflow.py",
                "Start web app: streamlit run app.py"
            ]


def main():
    """Main entry point"""
    verifier = SetupVerifier()
    success = verifier.run_all_checks()
    
    print("\n" + "="*70)
    print("  📋 RECOMMENDED NEXT STEPS")
    print("="*70 + "\n")
    
    for idx, step in enumerate(verifier.get_next_steps(), 1):
        print(f"{idx}. {step}")
    
    print("\n" + "="*70)
    print("  📚 HELPFUL RESOURCES")
    print("="*70)
    print("\nDocumentation:")
    print("  • ML_TRAINING_GUIDE.md - Complete training guide")
    print("  • ML_IMPLEMENTATION_SUMMARY.md - What was created")
    print("  • KAGGLE_DOWNLOAD_GUIDE.md - How to get datasets")
    print("  • quick_reference.py - 8 code examples")
    print("\nQuick Commands:")
    print("  • Verify setup: python setup_verification.py")
    print("  • Full training: python complete_workflow.py")
    print("  • Example usage: python quick_reference.py 1")
    print("  • Start app: streamlit run app.py")
    
    print("\n")
    return 0 if success or not verifier.issues else 1


if __name__ == "__main__":
    sys.exit(main())
