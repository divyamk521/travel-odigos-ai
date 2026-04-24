import json
from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.models.schemas import TravelResponse
from app.services.places_service import get_places
from app.services.budget_service import estimate_budget

client = Groq(api_key=settings.GROQ_API_KEY)
chat_memory = {}

def extract_json(text):
    try:
        # Finds the first { and last } to handle extra text from LLM
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != -1:
            return json.loads(text[start:end])
    except Exception as e:
        print(f"JSON Extraction Error: {e}")
    return None

def get_entities_from_message(message: str):
    """
    Uses the LLM to dynamically extract destination, days, and budget 
    from raw text. No more hardcoding!
    """
    system_prompt = """
    Extract travel entities from the user message. 
    Return ONLY JSON with keys: "destination", "days" (int), "budget" (budget/medium/luxury), "preferences" (list).
    If a value is missing, use null.
    """
    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0
        )
        entities = extract_json(response.choices[0].message.content)
        return entities
    except:
        return None

def generate_itinerary(data):
    """
    The core engine. Takes dynamic data, fetches real API results, 
    and returns a structured itinerary.
    """
    # 1. Fetch REAL-TIME data from your APIs based on user choice
    print(f"🌐 Fetching real-time data for: {data.destination}")
    places = get_places(data.destination)
    budget_info = estimate_budget(data.destination, data.days, data.budget)
    
    # 2. Safety Check: If APIs fail, we tell the user rather than hallucinating
    if not places:
        return {"error": f"I couldn't find real-time location data for '{data.destination}'. Please try a different city name."}

    # 3. Build the prompt with dynamic data
    prompt = build_itinerary_prompt(data, places, budget_info)

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a JSON travel generator. Use ONLY the provided verified places."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        return extract_json(response.choices[0].message.content)
            
    except Exception as e:
        return {"error": f"AI Generation failed: {str(e)}"}

def chat_with_ai(session_id: str, message: str):
    """
    Main Chat Entry Point. 
    Dynamically decides whether to plan a trip or just chat.
    """
    # 1. Ask the AI to identify the user's intent and entities
    entities = get_entities_from_message(message)
    
    # 2. If the user provided a destination, trigger the Dynamic Engine
    if entities and entities.get("destination"):
        # Convert dict to an object that generate_itinerary expects
        class DynamicData:
            def __init__(self, e):
                self.destination = e.get("destination")
                self.days = e.get("days") or 3
                self.budget = e.get("budget") or "medium"
                self.preferences = e.get("preferences") or []

        data = DynamicData(entities)
        return generate_itinerary(data)

    # 3. Fallback to general conversation if no trip intent is found
    if session_id not in chat_memory:
        chat_memory[session_id] = []

    history = chat_memory[session_id]
    history.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant. Help the user pick a destination."},
            *history[-5:]
        ]
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply