from fastapi import APIRouter
from app.models.schemas import TravelRequest, ChatRequest
from app.services.ai_service import generate_itinerary, chat_with_ai

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}



@router.post("/generate-itinerary")
def create_itinerary(request: TravelRequest):
    return generate_itinerary(request)



@router.post("/chat")
def chat(request: ChatRequest):
    response = chat_with_ai(request.session_id, request.message)
    return {"response": response}