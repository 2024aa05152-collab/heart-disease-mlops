from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd


# --------------------------------------------------
# Initialize FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Heart Disease Risk Prediction API",
    description="Predicts the risk of heart disease using a trained ML model",
    version="1.0"
)

# --------------------------------------------------
# Load trained model (includes preprocessing)
# --------------------------------------------------
model = joblib.load("models/heart_model.pkl")

# --------------------------------------------------
# Input schema (matches training features)
# --------------------------------------------------
class PatientData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int


# --------------------------------------------------
# Health check endpoint
# --------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "API is running"}


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------
@app.post("/predict")
def predict(data: PatientData):

    input_data = pd.DataFrame([{
        "age": data.age,
        "sex": data.sex,
        "cp": data.cp,
        "trestbps": data.trestbps,
        "chol": data.chol,
        "fbs": data.fbs,
        "restecg": data.restecg,
        "thalach": data.thalach,
        "exang": data.exang,
        "oldpeak": data.oldpeak,
        "slope": data.slope,
        "ca": data.ca,
        "thal": data.thal
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "heart_disease_risk": int(prediction),
        "risk_probability": round(float(probability), 3)
    }