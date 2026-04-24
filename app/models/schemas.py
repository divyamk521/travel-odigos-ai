from pydantic import BaseModel
from typing import List, Optional

class TravelRequest(BaseModel):
    destination: str
    days: int
    budget: str
    preferences: List[str] = []

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ItineraryDay(BaseModel):
    day: int
    theme: str
    description: str
    activities: List[str]

class TravelResponse(BaseModel):
    destination: str
    total_days: int
    summary: str
    itinerary: List[ItineraryDay]
    estimated_budget: str
    budget_analysis: str