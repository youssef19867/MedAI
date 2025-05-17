from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import uvicorn

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
try:
    text_model = joblib.load("disease_decision_tree_model4.pkl")
    image_model = tf.keras.models.load_model("best_skin_cnn__model_fold_2.keras")
    with open("model_feature_names.txt", "r") as f:
        feature_names = f.read().splitlines()
except Exception as e:
    raise RuntimeError(f"Failed to load models: {str(e)}")

# Class labels for image model
IMAGE_CLASSES = ['Eczema', 'Melanoma', 'Atopic Dermatitis', 'Normal']

def preprocess_image(image_bytes):
    """Convert uploaded image to model input format"""
    try:
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to grayscale and resize
        img = img.convert('L').resize((64, 64))
        
        # Convert to numpy array and normalize
        img_array = np.array(img) / 255.0
        
        # Add channel dimension
        img_array = np.expand_dims(img_array, axis=-1)
        
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")

@app.post("/predict-text")
async def predict_text(symptoms: dict):
    """Handle text-based symptom prediction"""
    try:
        # Create DataFrame with correct feature order
        ordered_features = {k: symptoms.get(k, 0) for k in feature_names}
        df = pd.DataFrame([ordered_features])
        
        # Make prediction
        prediction = text_model.predict(df)[0]
        proba = text_model.predict_proba(df)[0]
        confidence = round(max(proba), 4)
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": {cls: round(prob, 4) for cls, prob in zip(text_model.classes_, proba)}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    """Handle image-based prediction"""
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        img_array = preprocess_image(image_bytes)
        
        # Make prediction
        prediction = image_model.predict(np.array([img_array]))
        predicted_class = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        
        return {
            "prediction": IMAGE_CLASSES[predicted_class],
            "confidence": confidence,
            "class_index": predicted_class
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
