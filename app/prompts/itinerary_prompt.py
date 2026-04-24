# app/prompts/itinerary_prompt.py

def build_itinerary_prompt(data, places):
    """
    Constructs the prompt for the LLM using real-time place data.
    Handles both dictionary objects and simple strings safely.
    """
    formatted_places = []
    
    for p in places:
        # Check if the place is a dictionary (from Geoapify)
        if isinstance(p, dict):
            name = p.get('name', 'Unknown Attraction')
            cat = p.get('category', 'Tourist Spot')
            addr = p.get('address', 'Local area')
            formatted_places.append(f"- {name} ({cat}): {addr}")
        # Check if the place is just a string (from Fallback/Search)
        elif isinstance(p, str):
            formatted_places.append(f"- {p}")

    places_list = "\n".join(formatted_places)

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
2. The 'summary' should be an exciting 2-3 sentence intro welcoming the traveler.
3. The 'description' for each day must explain the narrative flow (e.g., "Start your morning at X before taking a scenic walk to Y").
4. The 'budget_analysis' should explain why this fits the {data.budget} budget level.
5. NEVER repeat an activity across different days.
6. Group activities geographically to minimize travel time.
7. Each day should have 3-4 activities.

Return ONLY a JSON object with this exact structure:
{{
  "destination": "{data.destination}",
  "total_days": {data.days},
  "summary": "English text...",
  "itinerary": [
    {{
      "day": number,
      "theme": "Theme Title",
      "description": "Daily narrative...",
      "activities": ["Activity 1", "Activity 2", "Activity 3"]
    }}
  ],
  "estimated_budget": "{data.budget}",
  "budget_analysis": "Detailed budget explanation..."
}}
"""