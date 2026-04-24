from groq import Groq
from app.core.config import settings
import json
import re

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_entities(message: str):
    prompt = f"""
Extract the following from the user message:

- destination (city or country)
- number of days (integer)
- budget (low, medium, luxury)

User message:
"{message}"

Return ONLY valid JSON:
{{
  "destination": "string or null",
  "days": number or null,
  "budget": "low/medium/luxury or null"
}}
"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You extract structured travel info."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
    except Exception:
        data = {
            "destination": None,
            "days": None,
            "budget": None
        }

    # 🔥 RULE-BASED FALLBACK (VERY IMPORTANT)

    msg_lower = message.lower()

    # extract days
    days_match = re.search(r'(\d+)\s*day', msg_lower)
    if days_match:
        data["days"] = int(days_match.group(1))

    # extract budget keywords
    if "cheap" in msg_lower or "low" in msg_lower:
        data["budget"] = "low"
    elif "luxury" in msg_lower:
        data["budget"] = "luxury"
    elif "medium" in msg_lower:
        data["budget"] = "medium"

    # extract destination (simple heuristic)
    words = message.split()
    if data["destination"] is None:
        # take last word as guess
        if len(words) > 0:
            data["destination"] = words[-1].capitalize()

    return data