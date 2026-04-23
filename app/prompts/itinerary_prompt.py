def build_itinerary_prompt(data, places):
    return f"""
You are a professional travel planner AI.

Create a detailed travel itinerary in STRICT JSON format.

User details:
- Starting location: {data.source}
- Destination: {data.destination}
- Number of days: {data.days}
- Budget: {data.budget}
- Preferences: {", ".join(data.preferences)}

Available places:
{places}

Rules:
- You MUST use these places in the itinerary
- Do NOT invent new place names
- Return ONLY valid JSON
- No explanations

Format:
{{
  "destination": "string",
  "total_days": number,
  "itinerary": [
    {{
      "day": number,
      "activities": ["activity1", "activity2"]
    }}
  ],
  "estimated_budget": "string"
}}
"""