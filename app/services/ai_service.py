from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.utils.json_utils import extract_json
from app.models.schemas import TravelResponse
from app.services.intent_service import detect_intent
from app.services.places_service import get_places
from app.services.budget_service import estimate_budget

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
    # 🔥 Detect intent
    intent = detect_intent(message)

    # 🔥 ROUTING LOGIC
    if intent == "budget":
        return estimate_budget("Goa", 3, "medium")

    elif intent == "places":
        return {"places": get_places("Goa")}

    elif intent == "itinerary":
        return {
            "message": "Please use /generate-itinerary endpoint for full plan."
        }

    # 🔹 Default chat
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