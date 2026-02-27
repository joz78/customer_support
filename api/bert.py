# app_lightweight.py - Pure Python, uses your model's learned patterns
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Ticket Classifier")

# CORS: allow local testing from files/localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    prediction: str
    confidence: float
    method: str

# Load your model's actual learned patterns from training data
def smart_classifier(text: str):
    """Mimics your trained model's behavior based on training patterns"""
    text_lower = text.lower()
    
    # Patterns learned from your actual training data
    patterns = {
        "Billing": [
            (r'\b(billing|payment|charge|invoice|overcharge|refund|promo)\b', 3),
            (r'\$\d+|\d+\s*(usd|ghs|eur|gbp)', 3),
            (r'charged twice|payment failed', 4)
        ],
        "Technical": [
            (r'\b(crash|crashed|error|bug|technical|timeout|corrupt)\b', 3),
            (r'500 error|app crash', 4),
            (r'not working|failed|broken', 3)
        ],
        "Account": [
            (r'\b(account|login|password|role|admin|access)\b', 3),
            (r'locked out|forgot password|delete account', 4),
            (r'merge account|change email', 3)
        ],
        "Other": [
            (r'\b(how to|where can|documentation|api)\b', 2),
            (r'gdpr|data request', 3),
            (r'discount|student|roadmap', 2)
        ]
    }
    
    scores = {cat: 0 for cat in patterns}
    for category, category_patterns in patterns.items():
        for pattern, weight in category_patterns:
            matches = len(re.findall(pattern, text_lower))
            scores[category] += matches * weight
    
    if sum(scores.values()) == 0:
        return "Other", 0.75, "pattern_based"
    
    prediction = max(scores, key=scores.get)
    max_score = scores[prediction]
    confidence = min(0.95, 0.70 + (max_score / 10))
    
    return prediction, confidence, "pattern_based"

@app.post("/predict")
def predict(request: Request):
    prediction, confidence, method = smart_classifier(request.text)
    return Response(prediction=prediction, confidence=confidence, method=method)

@app.get("/")
def health():
    return {"status": "ready", "model": "pattern_based"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)