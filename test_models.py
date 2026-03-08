"""Quick test of trained models"""
from model_integration import ModelManager

print("="*60)
print("  TESTING TRAINED ML MODELS")
print("="*60)

# Load models
manager = ModelManager()
print(f"\n✅ Models loaded: {manager.is_trained}")
print(f"📊 Stats: {manager.get_model_stats()}")

# Test predictions
test_resumes = [
    "Python Developer with 5 years experience in Django, Flask, SQL, and AWS",
    "Data Scientist with expertise in Machine Learning, TensorFlow, Python, R, and Statistics",
    "DevOps Engineer experienced in Kubernetes, Docker, Jenkins, and CI/CD pipelines"
]

print("\n" + "="*60)
print("  TEST PREDICTIONS")
print("="*60)

for resume in test_resumes:
    result = manager.predict_category(resume)
    if result:
        print(f"\n📄 Resume: {resume[:50]}...")
        print(f"   Category: {result['category']}")
        print(f"   Confidence: {result['confidence']:.1%}")
    else:
        print(f"\n⚠️  Prediction failed for: {resume[:50]}...")

print("\n" + "="*60)
print("✅ MODEL TESTS COMPLETE")
print("="*60)
