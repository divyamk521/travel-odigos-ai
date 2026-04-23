from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def detect_intent(message: str):
    prompt = f"""
Classify the user's intent into ONE of these:

- itinerary
- budget
- places
- general

User message:
"{message}"

Return ONLY one word from the list above.
"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an intent classifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    intent = response.choices[0].message.content.strip().lower()

    if intent not in ["itinerary", "budget", "places"]:
        return "general"

    return intent