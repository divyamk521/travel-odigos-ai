from fastapi import APIRouter
from app.models.schemas import TravelRequest
from app.services.ai_service import generate_itinerary

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/generate-itinerary")
def create_itinerary(request: TravelRequest):
    result = generate_itinerary(request)
    return result