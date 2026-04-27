#!/bin/bash

echo "🚀 Setting up Hate Speech Detection Backend..."

cd backend

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "🔤 Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
