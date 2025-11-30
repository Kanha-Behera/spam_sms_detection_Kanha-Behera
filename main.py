# backend/main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pickle
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
model = None

# Request model with validation
class Message(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="SMS text to classify")

# Response model
class PredictionResponse(BaseModel):
    result: str = Field(..., description="Classification result: 'Spam' or 'Ham'")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")

# Initialize FastAPI app
app = FastAPI(
    title="Spam SMS Detection API",
    description="Detect spam SMS messages using machine learning",
    version="1.0.0"
)

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Load model at startup"""
    global model
    try:
        model_path = "spam_model.pkl"
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        logger.info("✓ Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")

@app.get("/", tags=["Health"])
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Spam SMS Detection API",
        "status": "running",
        "model": "loaded" if model is not None else "not loaded"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    return {"status": "healthy", "model": "ready"}

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict_spam(data: Message):
    """
    Predict if an SMS is spam or ham (legitimate)
    
    Returns:
        - result: 'Spam' or 'Ham'
        - confidence: confidence score (0-1)
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please try again later."
        )
    
    try:
        # Get prediction and confidence
        prediction = model.predict([data.text])[0]
        confidence = max(model.predict_proba([data.text])[0])
        
        # Determine label
        label = "Spam" if prediction == 1 else "Ham"
        
        logger.info(f"Prediction: {label} (confidence: {confidence:.2%})")

        return PredictionResponse(
            result=label,
            confidence=float(confidence)
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@app.post("/batch-predict", tags=["Predictions"])
def batch_predict(messages: list[Message]):
    """
    Predict multiple SMS messages at once
    
    Args:
        messages: List of Message objects
        
    Returns:
        List of predictions with results and confidence scores
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        results = []
        for msg in messages:
            prediction = model.predict([msg.text])[0]
            confidence = max(model.predict_proba([msg.text])[0])
            label = "Spam" if prediction == 1 else "Ham"
            results.append({
                "text": msg.text[:50] + "..." if len(msg.text) > 50 else msg.text,
                "result": label,
                "confidence": float(confidence)
            })
        return {"predictions": results}
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
