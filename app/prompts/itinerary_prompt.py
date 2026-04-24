# app/prompts/itinerary_prompt.py

def build_itinerary_prompt(data, places):
    # Convert list of dicts to a readable string for the prompt
    places_list = "\n".join([f"- {p['name']} ({p['category']}): {p['address']}" for p in places])

    return f"""
You are an expert Luxury Travel Consultant. Your task is to create a highly engaging, logical, and descriptive travel itinerary.

--- TRIP DETAILS ---
Destination: {data.destination}
Duration: {data.days} Days
Budget Level: {data.budget}
Preferences: {", ".join(data.preferences) if data.preferences else "General Tourism"}

--- REAL-TIME VERIFIED PLACES ---
{places_list}

--- WRITING RULES ---
1. Use professional, welcoming English.
2. The 'summary' should be an exciting 2-3 sentence intro.
3. The 'description' for each day must explain the flow (e.g., "Start your morning at X before taking a scenic walk to Y").
4. The 'budget_analysis' should explain why this fits the {data.budget} budget.
5. NEVER repeat an activity across different days.
6. Group activities geographically to minimize travel time.

Return ONLY a JSON object with this exact structure:
{{
  "destination": "{data.destination}",
  "total_days": {data.days},
  "summary": "English text...",
  "itinerary": [
    {{
      "day": 1,
      "theme": "Historic Wonders & Landmarks",
      "description": "Detailed English narrative...",
      "activities": ["Activity Name 1", "Activity Name 2"]
    }}
  ],
  "estimated_budget": "{data.budget}",
  "budget_analysis": "Detailed English breakdown..."
}}
"""