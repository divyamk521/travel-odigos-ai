from pydantic import BaseModel, Field
from typing import List

class TravelRequest(BaseModel):
    source: str
    destination: str
    days: int = Field(..., gt=0, le=30)
    budget: str
    preferences: List[str]

class DayPlan(BaseModel):
    day: int
    activities: List[str]

class TravelResponse(BaseModel):
    destination: str
    total_days: int
    itinerary: List[DayPlan]
    estimated_budget: str