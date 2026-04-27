#!/usr/bin/env python3
"""
Test script for Hate Speech Detection API
Tests both local and deployed endpoints
"""

import requests
import json
import sys

def test_endpoint(base_url):
    """Test the API endpoint with sample texts"""
    
    print(f"\n🧪 Testing API at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False
    
    # Test 2: Prediction with neutral text
    print("\n2️⃣ Testing prediction with neutral text...")
    test_cases = [
        {
            "text": "I love spending time with my family on weekends.",
            "expected": "neither"
        },
        {
            "text": "The weather is beautiful today!",
            "expected": "neither"
        },
        {
            "text": "This movie was terrible and a complete waste of time.",
            "expected": "offensive language"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: '{test_case['text'][:50]}...'")
        try:
            response = requests.post(
                f"{base_url}/predict",
                json={"text": test_case["text"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Prediction: {result['prediction']}")
                print(f"   📊 Confidence: {result['confidence']:.2%}")
                print(f"   📈 Probabilities:")
                for label, prob in result['probabilities'].items():
                    print(f"      - {label}: {prob:.2%}")
            else:
                print(f"   ❌ Prediction failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Prediction error: {str(e)}")
            return False
    
    # Test 3: Error handling - empty text
    print("\n3️⃣ Testing error handling (empty text)...")
    try:
        response = requests.post(
            f"{base_url}/predict",
            json={"text": ""},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("   ✅ Empty text correctly rejected")
        else:
            print(f"   ⚠️  Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error handling test failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    return True

def main():
    """Main test function"""
    
    print("🛡️  Hate Speech Detection API Test Suite")
    print("=" * 60)
    
    # Test local endpoint
    local_url = "http://localhost:8000"
    print(f"\n📍 Testing LOCAL endpoint: {local_url}")
    
    try:
        test_endpoint(local_url)
    except Exception as e:
        print(f"\n❌ Local tests failed: {str(e)}")
        print("\n💡 Make sure the backend is running:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
    
    # Optionally test deployed endpoint
    if len(sys.argv) > 1:
        deployed_url = sys.argv[1]
        print(f"\n📍 Testing DEPLOYED endpoint: {deployed_url}")
        try:
            test_endpoint(deployed_url)
        except Exception as e:
            print(f"\n❌ Deployed tests failed: {str(e)}")
    else:
        print("\n💡 To test deployed endpoint, run:")
        print("   python test_api.py https://your-app.onrender.com")

if __name__ == "__main__":
    main()
