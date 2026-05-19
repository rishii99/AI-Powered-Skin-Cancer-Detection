from pydantic import BaseModel
from typing import List, Optional

class PredictionResult(BaseModel):
    label: str
    confidence: float

class PredictionResponse(BaseModel):
    primary: PredictionResult
    predictions: List[PredictionResult]
    confidence: float
    risk_level: str
    uncertain: bool
    gradcam: Optional[dict]

class FeedbackRequest(BaseModel):
    prediction_id: str
    helpful: bool
    comments: Optional[str] = None
