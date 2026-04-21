from groq import Groq
from app.core.config import settings
from app.prompts.itinerary_prompt import build_itinerary_prompt
from app.utils.json_utils import extract_json
from app.models.schemas import TravelResponse

client = Groq(api_key=settings.GROQ_API_KEY)

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
                        return validated.dict()
                except Exception as e:
                        return {
                         "error": "Validation failed",
                        "details": str(e),
                        "raw_output": parsed
                }
   