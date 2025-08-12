from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from hashlib import sha256
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os



# Load ML model and vectorizer
try:
    model = joblib.load("model/model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
except FileNotFoundError as e:
    raise RuntimeError(f"Required model files not found: {e}")

# Setup FastAPI app
app = FastAPI(title="Fake News Detector")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://172.29.165.116:27017")
client = MongoClient(MONGO_URI)
db = client["fake_news_db"]
collection = db["predictions"]

# Label map
LABEL_MAP = {0: "Fake", 1: "Real"}

# Request body schema
class NewsInput(BaseModel):
    text: str

# Response schema
class PredictionResponse(BaseModel):
    prediction: str
    source: str

# Helper: Hash the input to use as unique ID
def hash_text(text: str) -> str:
    return sha256(text.strip().lower().encode()).hexdigest()

@app.post("/predict", response_model=PredictionResponse)
def predict(news: NewsInput):
    input_text = news.text.strip()
    
    if not input_text:
        raise HTTPException(status_code=400, detail="Text input is empty.")

    hash_key = hash_text(input_text)

    # Check MongoDB cache
    existing = collection.find_one({"_id": hash_key})
    if existing:
        label = LABEL_MAP.get(existing["prediction"], "Unknown")
        return {"prediction": label, "source": "cache"}

    # Vectorize input and make prediction
    try:
        vectorized = vectorizer.transform([input_text])
        raw_prediction = int(model.predict(vectorized)[0])
        label = LABEL_MAP.get(raw_prediction, "Unknown")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    # Save to MongoDB
    collection.insert_one({
        "_id": hash_key,
        "text": input_text,
        "prediction": raw_prediction
    })

    return {"prediction": label, "source": "model"}
