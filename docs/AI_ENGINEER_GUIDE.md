# 🤖 AI Engineer Guide

## Model Architecture

**Bidirectional LSTM for Text Classification**

```python
# Architecture
Embedding(10000, 128) 
→ Bidirectional LSTM(64, return_sequences=True) 
→ Dropout(0.3)
→ Bidirectional LSTM(32) 
→ Dense(64, relu) 
→ Dropout(0.3)
→ Dense(3, softmax)

# Parameters
- Vocab Size: 10,000
- Sequence Length: 50 tokens
- Embedding Dim: 128
- Total Params: 1.7M
- Model Size: 17MB
```

## Training

```python
# Data
- Dataset: 24,783 tweets
- Classes: Hate Speech (5.8%), Offensive (77.4%), Neither (16.8%)
- Split: 80/20 train/test

# Optimization
- Optimizer: Adam (lr=0.001)
- Loss: Sparse Categorical Crossentropy
- Class Weights: Balanced (handles imbalance)
- Early Stopping: patience=5
- Batch Size: 64
- Epochs: 15 (with early stopping)

# Results
- Accuracy: 90%
- F1 Score: 0.90 (weighted)
- Inference: <100ms
```

## Preprocessing Pipeline

```python
def preprocess(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs, mentions, hashtags
    text = re.sub(r"http\S+|@\w+|#\w+", "", text)
    
    # 3. Keep only letters
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    
    # 4. Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    # 5. Tokenize (Keras Tokenizer)
    sequences = tokenizer.texts_to_sequences([text])
    
    # 6. Pad to 50 tokens
    padded = pad_sequences(sequences, maxlen=50, padding='pre')
    
    return padded
```

## Key Design Decisions

### 1. No Lemmatization/Stopwords
- **Why**: Simpler, faster, works well for short texts
- **Benefit**: 50% smaller memory footprint, no spaCy dependency

### 2. Class Weights vs SMOTE
- **Why**: Better generalization, faster training
- **Benefit**: No synthetic data, handles imbalance effectively

### 3. Bidirectional LSTM
- **Why**: Captures context from both directions
- **Benefit**: Better understanding of tweet context

### 4. Dropout (0.3)
- **Why**: Prevents overfitting on imbalanced data
- **Benefit**: Better generalization to unseen data

## API Implementation

```python
# FastAPI with async
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Preprocess
    processed = preprocess_text(request.text)
    
    # Predict
    probs = model.predict(processed, verbose=0)[0]
    predicted_class = int(probs.argmax())
    
    return {
        "prediction": LABEL_MAP[predicted_class],
        "confidence": float(probs[predicted_class]),
        "probabilities": {
            "hate_speech": float(probs[0]),
            "offensive_language": float(probs[1]),
            "neither": float(probs[2])
        }
    }
```

## Performance Optimization

### Memory
- TensorFlow CPU-only: ~400MB
- Model loaded once on startup
- Fits in 512MB free tier

### Speed
- Inference: <100ms
- API Response: <500ms
- Async processing for concurrency

### Deployment
- Backend: Render (Python 3.12)
- Frontend: Vercel (React 18)
- Auto-scaling enabled

## Model Files

```
backend/
├── model.h5           # Trained model (17MB)
├── tokenizer.pkl      # Keras Tokenizer (1.4MB)
└── seq_len.pkl        # Sequence length (50)
```

## Reproducing Training

```python
# 1. Load data
df = pd.read_csv('data/hate_speech_detection.csv')

# 2. Preprocess
df['clean_tweet'] = df['tweet'].apply(clean_text)

# 3. Tokenize
tokenizer = Tokenizer(num_words=10000, oov_token="<unk>")
tokenizer.fit_on_texts(df['clean_tweet'])
sequences = tokenizer.texts_to_sequences(df['clean_tweet'])
X = pad_sequences(sequences, maxlen=50, padding='pre')
y = df['class'].values

# 4. Class weights
class_weights = compute_class_weight('balanced', 
                                     classes=np.unique(y), 
                                     y=y)

# 5. Train
model.fit(X_train, y_train,
          epochs=15,
          batch_size=64,
          validation_split=0.1,
          class_weight=dict(enumerate(class_weights)),
          callbacks=[early_stopping])

# 6. Save
model.save('model.h5')
pickle.dump(tokenizer, open('tokenizer.pkl', 'wb'))
pickle.dump(50, open('seq_len.pkl', 'wb'))
```

## Evaluation Metrics

```python
# Classification Report
                    precision  recall  f1-score
hate speech            0.85     0.72     0.78
offensive language     0.92     0.96     0.94
neither                0.78     0.65     0.71

accuracy                                 0.90
weighted avg           0.90     0.90     0.90
```

## Improvements to Consider

1. **Model Architecture**
   - Try Transformer-based models (BERT, RoBERTa)
   - Experiment with CNN-LSTM hybrid
   - Add attention mechanism

2. **Data**
   - Collect more hate speech examples (currently 5.8%)
   - Add data augmentation
   - Use active learning

3. **Features**
   - Add character-level features
   - Include user metadata
   - Multi-task learning

4. **Deployment**
   - Add model versioning
   - Implement A/B testing
   - Add monitoring & logging

## Testing

```bash
# Unit tests
cd tests
python test_api.py

# Load testing
ab -n 1000 -c 10 http://localhost:8000/predict

# Model evaluation
python evaluate_model.py
```

## Monitoring

```python
# Track in production
- Prediction distribution
- Confidence scores
- Response times
- Error rates
- Model drift
```

## References

- Dataset: Twitter Hate Speech Dataset
- Framework: TensorFlow/Keras
- Deployment: Render + Vercel
- Code: See `backend/main.py`

## Quick Commands

```bash
# Train model
python train_model.py

# Evaluate
python evaluate_model.py

# Start API
uvicorn main:app --reload

# Test
python test_api.py
```

---

**Built for production ML deployment with focus on simplicity and performance.**
