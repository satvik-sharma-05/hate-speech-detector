# 📁 Project Structure

```
hate-speech-detection/
│
├── backend/                    # Backend API
│   ├── main.py                # FastAPI application
│   ├── model.h5               # Trained LSTM model (17MB)
│   ├── tokenizer.json         # Keras tokenizer (JSON format)
│   ├── seq_len.pkl            # Sequence length (50)
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-render.txt # Deployment dependencies
│   └── .gitignore             # Git ignore rules
│
├── frontend/                   # Frontend UI
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Styles & animations
│   │   └── main.jsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── vercel.json            # Vercel deployment config
│   └── .env.example           # Environment variables template
│
├── data/                       # Dataset & Training
│   ├── hate_speech_detection.csv
│   └── Hate_Speech_Detection_using_LSTM (1).ipynb
│
├── tests/                      # Test Files
│   ├── test_api.py            # API endpoint tests
│   ├── test_exact_samples.py  # Sample prediction tests
│   └── final_comprehensive_test.py
│
├── scripts/                    # Setup Scripts
│   ├── setup_backend.bat      # Windows backend setup
│   ├── setup_backend.sh       # Unix backend setup
│   ├── setup_frontend.bat     # Windows frontend setup
│   └── setup_frontend.sh      # Unix frontend setup
│
├── docs/                       # Documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── DEPLOYMENT.md          # Deployment instructions
│   ├── AI_ENGINEER_GUIDE.md   # Model architecture & training
│   ├── DEVELOPER_DOCUMENTATION.md  # Complete technical guide
│   └── PROJECT_STRUCTURE.md   # This file
│
├── correctModels/              # Correct trained models
│   ├── model.h5
│   ├── tokenizer.json
│   ├── seq_len.pkl
│   └── Hate_Speech_Detection_using_LSTM (1).ipynb
│
├── .gitignore                  # Git ignore rules
├── .python-version             # Python version (3.10.0)
├── runtime.txt                 # Render Python version
├── render.yaml                 # Render deployment config
└── README.md                   # Main documentation
```

## 🌐 Live Deployment

- **Frontend**: https://hate-speech-detector-sigma.vercel.app/
- **Backend API**: https://hate-speech-detector-backend-oamo.onrender.com
- **API Docs**: https://hate-speech-detector-backend-oamo.onrender.com/docs

## 📦 Key Files

### Backend
- **main.py**: FastAPI application with prediction endpoint
- **model.h5**: Bidirectional LSTM model (1.7M parameters)
- **tokenizer.json**: Keras tokenizer (10K vocab, JSON format for compatibility)
- **seq_len.pkl**: Sequence length configuration (50 tokens)
- **requirements-render.txt**: Optimized for 512MB deployment

### Frontend
- **App.jsx**: React component with state management
- **App.css**: Modern CSS with animations and responsive design
- **vercel.json**: Vercel deployment configuration

### Documentation
- **QUICKSTART.md**: Get started in 5 minutes
- **DEPLOYMENT.md**: Production deployment guide
- **AI_ENGINEER_GUIDE.md**: Model architecture and training details
- **DEVELOPER_DOCUMENTATION.md**: Complete technical implementation

## 🚀 Quick Commands

```bash
# Start Backend (Local)
cd backend && python -m uvicorn main:app --reload

# Start Frontend (Local)
cd frontend && npm run dev

# Run Tests
cd tests && python test_api.py

# Deploy Backend
git push origin main  # Auto-deploys to Render

# Deploy Frontend
cd frontend && vercel --prod
```

## 📊 File Sizes

| File | Size | Purpose |
|------|------|---------|
| model.h5 | 17 MB | Trained LSTM model |
| tokenizer.json | 1.4 MB | Word-to-index mapping |
| seq_len.pkl | <1 KB | Sequence length config |
| main.py | ~5 KB | Backend API code |
| App.jsx | ~10 KB | Frontend React code |

## 🔧 Technology Stack

**Backend:**
- Python 3.10
- FastAPI 0.95.2
- TensorFlow 2.13.0
- Keras 2.13.1
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Vite (build tool)
- Axios (HTTP client)
- Modern CSS3

**Deployment:**
- Render (backend)
- Vercel (frontend)
- GitHub (version control)

## 📖 Documentation Links

- [README.md](../README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [AI_ENGINEER_GUIDE.md](AI_ENGINEER_GUIDE.md) - Model details
- [DEVELOPER_DOCUMENTATION.md](DEVELOPER_DOCUMENTATION.md) - Technical guide
