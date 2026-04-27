# 🛡️ Hate Speech Detection System

Real-time hate speech detection using Bidirectional LSTM neural network. Classifies text into: Hate Speech, Offensive Language, or Neither.

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Runs on http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on http://localhost:3000

## 📊 Tech Stack

- **ML**: Bidirectional LSTM (TensorFlow/Keras)
- **Backend**: FastAPI + Python 3.12
- **Frontend**: React 18 + Vite
- **Accuracy**: 90%

## 📁 Project Structure

```
├── backend/          # FastAPI application
├── frontend/         # React application
├── data/             # Dataset & notebook
├── tests/            # Test files
├── scripts/          # Setup scripts
└── docs/             # Documentation
```

## 🧪 Testing

```bash
cd tests
python test_api.py
```

## 📖 Documentation

- [Quick Start](docs/QUICKSTART.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [AI Engineer Guide](docs/AI_ENGINEER_GUIDE.md) - Model architecture & training
- [Developer Documentation](docs/DEVELOPER_DOCUMENTATION.md) - Complete technical guide

## 🎯 Features

- Real-time text analysis
- 3-class classification
- Confidence scores with probability bars
- Modern responsive UI
- <500ms API response time

## 📝 License

MIT
