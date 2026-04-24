def build_itinerary_prompt(data, places, budget_info):
    """
    Constructs the prompt for the LLM using real-time place data and budget intelligence.
    Ensures the AI stays locked to the requested destination.
    """
    formatted_places = []
    
    for p in places:
        if isinstance(p, dict):
            name = p.get('name', 'Attraction')
            cat = p.get('category', 'Sights')
            addr = p.get('address', 'Local area')
            formatted_places.append(f"- {name} ({cat}): {addr}")
        else:
            formatted_places.append(f"- {p}")

    places_list = "\n".join(formatted_places)

    return f"""
### MANDATORY INSTRUCTIONS ###
- YOU ARE A LOCAL TRAVEL EXPERT FOR {data.destination.upper()}.
- YOU MUST ONLY USE THE PLACES LISTED UNDER 'VERIFIED PLACES'.
- DO NOT MENTION PARIS, LONDON, OR ANY OTHER CITY. 
- IF THE DESTINATION IS {data.destination}, EVERY ACTIVITY MUST BE IN {data.destination}.

--- TRIP CORE ---
Destination: {data.destination}
Duration: {data.days} Days
Budget Level: {data.budget}
User Preferences: {", ".join(data.preferences) if data.preferences else "General Sightseeing"}

--- FINANCIAL DATA (MUST BE USED IN BUDGET ANALYSIS) ---
Total Trip Cost: {budget_info['total_cost']} {budget_info['currency']}
Average Hotel/Night: {budget_info['daily_hotel']} {budget_info['currency']}
Daily Allowance (Food/Travel): {budget_info['daily_allowance']} {budget_info['currency']}

--- VERIFIED PLACES FOR {data.destination} ---
{places_list}

--- WRITING RULES ---
1. Language: Professional, welcoming English.
2. The 'summary' must be 2-3 sentences specifically about visiting {data.destination}.
3. The 'budget_analysis' must explain how the {budget_info['total_cost']} {budget_info['currency']} covers the specific {data.days}-day stay.
4. Each day must have 3-4 activities grouped geographically.

--- OUTPUT FORMAT ---
Return ONLY a valid JSON object. 

{{
  "destination": "{data.destination}",
  "total_days": {data.days},
  "summary": "...",
  "itinerary": [
    {{
      "day": 1,
      "theme": "Theme Title",
      "description": "Narrative description of the day...",
      "activities": ["Activity 1", "Activity 2", "Activity 3"]
    }}
  ],
  "estimated_budget": "{budget_info['total_cost']} {budget_info['currency']}",
  "budget_analysis": "..."
}}
"""