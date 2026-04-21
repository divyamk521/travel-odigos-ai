from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
import json

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_itinerary(data):
    prompt = build_itinerary_prompt(data)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,  
        messages=[
            {"role": "system", "content": "You are a travel planning assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        return parsed
    except Exception:
        return {
            "error": "Failed to parse AI response",
            "raw_output": content
        }