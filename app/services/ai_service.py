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
    places = get_places(data.destination)
    prompt = build_itinerary_prompt(data, places)

    for attempt in range(3):
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        parsed = extract_json(content)

        if parsed:
            try:
                validated = TravelResponse(**parsed)
                return validated.model_dump()
            except Exception:
                continue

    return {"error": "Failed to generate itinerary"}


def chat_with_ai(session_id: str, message: str):
    # 🔥 Step 1: detect intent
    intent = detect_intent(message)

    # 🔥 Step 2: extract entities
    entities = extract_entities(message)

    destination = entities.get("destination") or "Goa"
    days = entities.get("days") or 3
    budget = entities.get("budget") or "medium"

    # 🔥 Step 3: route based on intent

    if intent == "budget":
        return estimate_budget(destination, days, budget)

    elif intent == "places":
        return {"places": get_places(destination)}

    elif intent == "itinerary":
        data = type("obj", (object,), {
            "source": "unknown",
            "destination": destination,
            "days": days,
            "budget": budget,
            "preferences": []
        })()

        return generate_itinerary(data)

    # 🔹 fallback chat
    if session_id not in chat_memory:
        chat_memory[session_id] = []

    history = chat_memory[session_id]

    history.append({"role": "user", "content": message})
    history = trim_memory(history)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            *history
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content

    history.append({"role": "assistant", "content": reply})
    history = trim_memory(history)

    chat_memory[session_id] = history

    return {"response": reply}