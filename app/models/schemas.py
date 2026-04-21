from pydantic import BaseModel, Field
from typing import List


# 🔹 Request Schema (input from user / backend)
class TravelRequest(BaseModel):
    source: str = Field(..., min_length=1, description="Starting location")
    destination: str = Field(..., min_length=1, description="Travel destination")
    days: int = Field(..., gt=0, le=30, description="Number of travel days")
    budget: str = Field(..., min_length=1, description="Budget type (low, medium, luxury)")
    preferences: List[str] = Field(default_factory=list, description="User interests")


# 🔹 Each day's plan
class DayPlan(BaseModel):
    day: int = Field(..., ge=1, description="Day number")
    activities: List[str] = Field(..., min_items=1, description="List of activities")


# 🔹 Final AI Response Schema (validated output)
class TravelResponse(BaseModel):
    destination: str
    total_days: int = Field(..., ge=1, le=30)
    itinerary: List[DayPlan]
    estimated_budget: str