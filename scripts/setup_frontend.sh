#!/bin/bash

echo "🚀 Setting up Hate Speech Detection Frontend..."

cd frontend

# Install dependencies
echo "📥 Installing dependencies..."
npm install

# Create .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your backend URL"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "To start the frontend development server:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "To build for production:"
echo "  npm run build"
