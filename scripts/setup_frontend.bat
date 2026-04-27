@echo off
echo 🚀 Setting up Hate Speech Detection Frontend...

cd frontend

REM Install dependencies
echo 📥 Installing dependencies...
call npm install

REM Create .env file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please update .env with your backend URL
) else (
    echo ✅ .env file already exists
)

echo.
echo ✅ Frontend setup complete!
echo.
echo To start the frontend development server:
echo   cd frontend
echo   npm run dev
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo To build for production:
echo   npm run build

pause
