from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import mlflow
import os

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Customer Ticket Classifier API", version="1.0")

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Dynamically find the model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "models", "model (2).pkl"))

# Load model
model = joblib.load(MODEL_PATH)


pipeline = model.best_estimator_ if hasattr(model, "best_estimator_") else model

#  LABEL MAPPING 
label_mapping = {
    0: "Account",
    1: "Billing",
    2: "Other",
    3: "Technical"
}

mlflow.set_tracking_uri("file:./mlruns")

class TicketInput(BaseModel):
    message: str

@app.post("/predict")
def predict(data: TicketInput):
    text = data.message

    # Get numeric prediction
    pred_index = int(pipeline.predict([text])[0])

    # Convert to original class name
    prediction = label_mapping[pred_index]

    # Get probabilities
    probas = pipeline.predict_proba([text])[0]

    # Convert probabilities to readable labels
    confidence = {
        label_mapping[i]: float(prob)
        for i, prob in enumerate(probas)
    }

    return {
        "input": text,
        "predicted_class": prediction,
        "confidence_scores": confidence
    }
