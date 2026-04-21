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
    activities: List[str] = Field(..., min_items=1)



class TravelResponse(BaseModel):
    destination: str
    total_days: int = Field(..., ge=1, le=30)
    itinerary: List[DayPlan]
    estimated_budget: str



class ChatRequest(BaseModel):
    session_id: str
    message: str



class ChatResponse(BaseModel):
    response: str