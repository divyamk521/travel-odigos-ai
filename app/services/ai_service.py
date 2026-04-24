# app/services/ai_service.py
from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.utils.json_utils import extract_json
from app.models.schemas import TravelResponse
from app.services.intent_service import detect_intent
from app.services.places_service import get_places
from app.services.budget_service import estimate_budget
from app.services.entity_service import extract_entities

client = Groq(api_key=settings.GROQ_API_KEY)

chat_memory = {}

def trim_memory(history):
    limit = settings.MEMORY_LIMIT
    if len(history) > limit:
        return history[-limit:]
    return history

def generate_itinerary(data):
    # This now calls our Geoapify-powered service
    places = get_places(data.destination)

    print("\n📍 REAL-TIME PLACES FETCHED:", places)

    # If Geoapify and Fallback both fail to find 5 spots
    if len(places) < 5:
        return {
            "error": f"I couldn't find enough verified attractions for {data.destination} right now."
        }

    # Pass the structured real-world data into your prompt builder
    prompt = build_itinerary_prompt(data, places)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional travel planner. Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )

            content = response.choices[0].message.content
            print(f"\n🔍 LLM ATTEMPT {attempt + 1} OUTPUT:\n", content)

            parsed = extract_json(content)

            if parsed:
                # Validate against your Pydantic schema
                validated = TravelResponse(**parsed)
                return validated.model_dump()
                
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")

    return {
        "error": "Failed to generate a valid itinerary after 3 attempts.",
        "raw_output": content if 'content' in locals() else "No response"
    }

def chat_with_ai(session_id: str, message: str):
    # 1. Understand what the user wants
    intent = detect_intent(message)
    entities = extract_entities(message)

    destination = entities.get("destination")
    
    # 2. If it's a planning task, we need a destination
    if intent in ["itinerary", "places", "budget"] and not destination:
        return {"response": "That sounds like a great plan! Which city or country are you thinking of visiting?"}

    days = entities.get("days") or 3
    budget = entities.get("budget") or "medium"

    # 3. Route to specific services based on Intent
    if intent == "budget":
        return estimate_budget(destination, days, budget)

    elif intent == "places":
        real_places = get_places(destination)
        return {
            "destination": destination,
            "places": real_places,
            "message": f"Here are some top-rated spots in {destination} right now."
        }

    elif intent == "itinerary":
        # Create a simple data object for generate_itinerary
        class TravelData:
            def __init__(self, d, dy, b):
                self.destination = d
                self.days = dy
                self.budget = b
                self.preferences = []
        
        data = TravelData(destination, days, budget)
        return generate_itinerary(data)

    # 4. General Chat (Memory Management)
    if session_id not in chat_memory:
        chat_memory[session_id] = []

    history = chat_memory[session_id]
    history.append({"role": "user", "content": message})
    history = trim_memory(history)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant. You have access to real-time data when users ask for plans."},
            *history
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    chat_memory[session_id] = trim_memory(history)

    return {"response": reply}