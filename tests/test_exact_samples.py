#!/usr/bin/env python3
"""
Test with the exact same samples from the notebook
"""

import requests
import json

def test_text(text):
    """Test a single text"""
    response = requests.post(
        "http://localhost:8000/predict",
        json={"text": text},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Sentence: '{text}'")
        print(f"Prediction: {result['prediction']}\n")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Exact samples from the notebook
sample_sentences = [
    "You are so stupid and ugly.",
    "That's a really great idea!",
    "I hate your guts, you're worthless.",
    "This movie is just okay.",
    "Go to hell, you filthy animal.",
    "I am so happy today.",
    "You call that art? It's trash!",
    "What a beautiful day.",
    "I will break your face if you ever talk to me again.",
    "The weather forecast predicts rain tomorrow."
]

print("=" * 60)
print("Testing with Exact Notebook Samples")
print("=" * 60)
print()

for text in sample_sentences:
    test_text(text)

print("=" * 60)
