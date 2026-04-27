from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import pickle
import json
import os
import sys
import re
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and preprocessing
model = None
tokenizer = None
sentence_length = None

# Label mapping
LABEL_MAP = {
    0: "hate speech",
    1: "offensive language",
    2: "neither"
}

def clean_text(text):
    """
    Clean text using the same function as in the notebook
    """
    text = text.lower()
    text = re.sub(r"http\S+|@\w+|#\w+", "", text)  # remove links, mentions
    text = re.sub(r"[^a-zA-Z\s]", "", text)        # keep words only
    text = re.sub(r"\s+", " ", text).strip()
    return text

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model and preprocessing components on startup"""
    global model, tokenizer, sentence_length
    
    try:
        # Load sequence length
        logger.info("Loading sequence length...")
        seq_len_path = 'seq_len.pkl'
        if not os.path.exists(seq_len_path):
            seq_len_path = '../seq_len.pkl'
        
        with open(seq_len_path, 'rb') as f:
            sentence_length = pickle.load(f)
        logger.info(f"Sequence length loaded: {sentence_length}")
        
        # Load tokenizer from JSON
        logger.info("Loading tokenizer...")
        tokenizer_path = 'tokenizer.json'
        if not os.path.exists(tokenizer_path):
            tokenizer_path = '../tokenizer.json'
        
        with open(tokenizer_path, 'r') as f:
            tokenizer_json = f.read()
            tokenizer = tokenizer_from_json(tokenizer_json)
        logger.info("Tokenizer loaded successfully from JSON")
        
        # Load Keras model (H5 format compatible with TF 2.13)
        logger.info("Loading Keras model...")
        model_path = 'model.h5'
        if not os.path.exists(model_path):
            model_path = '../model.h5'
        
        logger.info(f"Model path: {model_path}")
        logger.info(f"Model file exists: {os.path.exists(model_path)}")
        
        # Load without compiling to avoid optimizer deserialization issues
        model = tf.keras.models.load_model(model_path, compile=False)
        logger.info("Model loaded successfully")
        logger.info("Startup complete!")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}", exc_info=True)
        # DO NOT raise - let the app start anyway so port opens
    
    yield
    
    # Cleanup (if needed)
    logger.info("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="Hate Speech Detection API",
    description="API for detecting hate speech, offensive language, and neutral content",
    version="2.0.0",
    lifespan=lifespan
)

# Add startup event for logging
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app starting up...")
    logger.info(f"Python version: {os.sys.version}")
    logger.info(f"TensorFlow version: {tf.__version__}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Files in current directory: {os.listdir('.')}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    text: str
    prediction: str
    confidence: float
    probabilities: dict

def preprocess_text(text: str) -> list:
    """
    Preprocess text following the exact training pipeline:
    1. Clean text (lowercase, remove links/mentions, keep only letters)
    2. Tokenize using Keras Tokenizer
    3. Padding
    """
    # Step 1: Clean text
    processed_text = clean_text(text)
    
    # Step 2: Tokenize
    sequences = tokenizer.texts_to_sequences([processed_text])
    
    # Step 3: Padding
    padded = pad_sequences(sequences, padding='pre', maxlen=sentence_length)
    
    return padded

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Hate Speech Detection API is operational",
        "version": "2.0.0"
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint to ensure port is open"""
    return {"status": "alive"}

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None,
        "sentence_length": sentence_length
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict hate speech, offensive language, or neither for given text
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Preprocess the input text
        processed_input = preprocess_text(request.text)
        
        # Make prediction
        prediction_probs = model.predict(processed_input, verbose=0)[0]
        predicted_class = int(prediction_probs.argmax())
        confidence = float(prediction_probs[predicted_class])
        
        # Prepare response
        probabilities = {
            "hate_speech": float(prediction_probs[0]),
            "offensive_language": float(prediction_probs[1]),
            "neither": float(prediction_probs[2])
        }
        
        return PredictionResponse(
            text=request.text,
            prediction=LABEL_MAP[predicted_class],
            confidence=confidence,
            probabilities=probabilities
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
