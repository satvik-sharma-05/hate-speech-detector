# 📁 Project Structure

```
hate-speech-detection/
│
├── backend/                    # Backend API
│   ├── main.py                # FastAPI application
│   ├── model.h5               # Trained LSTM model
│   ├── tokenizer.pkl          # Keras tokenizer
│   ├── seq_len.pkl            # Sequence length
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-render.txt # Deployment dependencies
│   └── render.yaml            # Render config
│
├── frontend/                   # Frontend UI
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── App.css            # Styles
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite config
│   └── vercel.json            # Vercel config
│
├── data/                       # Dataset & Training
│   ├── hate_speech_detection.csv
│   └── Hate_Speech_Detection_using_LSTM (1).ipynb
│
├── tests/                      # Test Files
│   ├── test_api.py
│   ├── test_exact_samples.py
│   └── final_comprehensive_test.py
│
├── scripts/                    # Setup Scripts
│   ├── setup_backend.bat
│   ├── setup_backend.sh
│   ├── setup_frontend.bat
│   └── setup_frontend.sh
│
├── docs/                       # Documentation
│   ├── DEPLOYMENT.md
│   └── DEVELOPER_DOCUMENTATION.md
│
├── .gitignore
└── README.md                   # Main documentation
```

## Quick Commands

```bash
# Start Backend
cd backend && python -m uvicorn main:app --reload

# Start Frontend  
cd frontend && npm run dev

# Run Tests
cd tests && python test_api.py

# Deploy
# See docs/DEPLOYMENT.md
```
