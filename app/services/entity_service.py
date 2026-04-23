from groq import Groq
from app.core.config import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_entities(message: str):
    prompt = f"""
Extract the following from the user message:

- destination
- number of days
- budget (low, medium, luxury)

User message:
"{message}"

Return ONLY valid JSON like:
{{
  "destination": "string",
  "days": number,
  "budget": "string"
}}

If something is missing, return null for that field.
"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You extract structured data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "destination": None,
            "days": None,
            "budget": None
        }