from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Prediction API")

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
model = None

class PredictionRequest(BaseModel):
    user_id: str
    features_for_prediction: list[float] = Field(min_items=1)

class PredictionResponse(BaseModel):
    user_id: str
    prediction_score: float
    model_version: str

@app.on_event("startup")
def load_model():
    global model
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        logging.info("Model loaded")
    except Exception as e:
        logging.error(f"Model load failed: {e}")

@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if len(req.features_for_prediction) != model.n_features_in_:
        raise HTTPException(status_code=400, detail="Incorrect feature count")

    try:
        score = model.predict_proba([req.features_for_prediction])[0][1]
        return PredictionResponse(
            user_id=req.user_id,
            prediction_score=float(score),
            model_version=MODEL_VERSION,
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Prediction failed")
