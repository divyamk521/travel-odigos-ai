from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.utils.json_utils import extract_json
from app.models.schemas import TravelResponse

client = Groq(api_key=settings.GROQ_API_KEY)

# 🔹 In-memory chat storage
chat_memory = {}


# 🔹 Itinerary Generator
def generate_itinerary(data):
    prompt = build_itinerary_prompt(data)

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

    return {
        "error": "Failed to generate valid itinerary",
        "raw_output": content
    }


# 🔹 Chat Function with Memory
def chat_with_ai(session_id: str, message: str):
    if session_id not in chat_memory:
        chat_memory[session_id] = []

    # Add user message
    chat_memory[session_id].append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            *chat_memory[session_id]
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content

    # Store AI reply
    chat_memory[session_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply