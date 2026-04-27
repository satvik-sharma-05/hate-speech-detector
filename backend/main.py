from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
import os
import re
import logging
import sys
import json
from contextlib import asynccontextmanager

# Fix for Keras pickle compatibility
class KerasUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Handle legacy Keras imports
        if 'keras.src' in module:
            module = module.replace('keras.src', 'keras')
        if module.startswith('keras.') and not module.startswith('tensorflow.keras'):
            module = 'tensorflow.' + module
        return super().find_class(module, name)

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
        
        # Load tokenizer with multiple fallback strategies
        logger.info("Loading tokenizer...")
        tokenizer_path = 'tokenizer.pkl'
        if not os.path.exists(tokenizer_path):
            tokenizer_path = '../tokenizer.pkl'
        
        tokenizer_loaded = False
        
        # Strategy 1: Try custom unpickler
        try:
            with open(tokenizer_path, 'rb') as f:
                tokenizer = KerasUnpickler(f).load()
            logger.info("Tokenizer loaded with custom unpickler")
            tokenizer_loaded = True
        except Exception as e:
            logger.warning(f"Custom unpickler failed: {e}")
        
        # Strategy 2: Try standard pickle with sys.modules patching
        if not tokenizer_loaded:
            try:
                # Patch sys.modules to handle keras imports
                import keras
                sys.modules['keras.src.legacy'] = keras.legacy
                sys.modules['keras.src.legacy.preprocessing'] = keras.preprocessing
                sys.modules['keras.src.legacy.preprocessing.text'] = keras.preprocessing.text
                
                with open(tokenizer_path, 'rb') as f:
                    tokenizer = pickle.load(f)
                logger.info("Tokenizer loaded with sys.modules patching")
                tokenizer_loaded = True
            except Exception as e:
                logger.warning(f"Sys.modules patching failed: {e}")
        
        # Strategy 3: Create new tokenizer from vocab (if tokenizer has word_index)
        if not tokenizer_loaded:
            logger.warning("All loading strategies failed. Creating new tokenizer from scratch.")
            # This is a fallback - you'll need to ensure vocab_size matches training
            tokenizer = Tokenizer(num_words=10000, oov_token="<unk>")
            # Note: This won't have the exact same word_index as training
            # You should regenerate tokenizer.pkl with compatible Keras version
            logger.error("WARNING: Using fresh tokenizer - predictions may be inaccurate!")
            logger.error("Please regenerate tokenizer.pkl with TensorFlow 2.15.0")
        
        # Load Keras model
        logger.info("Loading Keras model...")
        model_path = 'model.h5'
        if not os.path.exists(model_path):
            model_path = '../model.h5'
        
        model = tf.keras.models.load_model(model_path)
        logger.info("Model loaded successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
