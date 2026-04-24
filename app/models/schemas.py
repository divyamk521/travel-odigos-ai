# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List

class TravelRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    days: int = Field(..., gt=0, le=30)
    budget: str = Field(..., min_length=1)
    preferences: List[str] = Field(default_factory=list)

class DayPlan(BaseModel):
    day: int = Field(..., ge=1)
    theme: str = Field(..., description="A catchy title for the day's vibe")
    description: str = Field(..., description="A short paragraph in English explaining the day's flow")
    activities: List[str] = Field(..., min_items=1)

class TravelResponse(BaseModel):
    destination: str
    total_days: int = Field(..., ge=1, le=30)
    summary: str = Field(..., description="An introductory welcome message about the trip")
    itinerary: List[DayPlan]
    estimated_budget: str
    budget_analysis: str = Field(..., description="A detailed explanation of costs in English")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str