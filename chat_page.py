from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add this import
import joblib
import pandas as pd

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load features and model
with open("model_feature_names.txt", "r") as f:
    feature_names = f.read().splitlines()
model = joblib.load("disease_decision_tree_model4.pkl")

# Add get_features endpoint
@app.get("/get_features")
def get_features():
    return feature_names  # Return feature names as questions

@app.post("/predict")
def predict_disease(symptoms: dict):
    new_input = pd.DataFrame([symptoms], columns=feature_names)
    prediction = model.predict(new_input)[0]
    probabilities = model.predict_proba(new_input)
    confidence = max(probabilities[0])
    return {"prediction": prediction, "confidence": round(confidence, 2)}  # Fix key name
