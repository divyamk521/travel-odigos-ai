# app/services/places_service.py
import requests
import json
from groq import Groq
from app.core.config import settings
from app.services.search_service import get_city_coordinates

client = Groq(api_key=settings.GROQ_API_KEY)

def get_places(destination: str):
    """
    Fetches 10-15 REAL tourist attractions using Geoapify.
    Falls back to Groq if the API fails or returns no data.
    """
    # 1. Get Coordinates first
    lat, lon = get_city_coordinates(destination)
    
    if lat is None or lon is None:
        return generate_fallback_places(destination)

    # 2. Fetch Places from Geoapify
    # Categories: sights, culture, monuments, parks
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "tourism.sights,entertainment.culture,leisure.park",
        "filter": f"circle:{lon},{lat},15000",  # 15km radius
        "bias": f"proximity:{lon},{lat}",
        "limit": 15,
        "apiKey": settings.GEOAPIFY_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        places = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            if props.get("name"):
                places.append({
                    "name": props.get("name"),
                    "address": props.get("address_line2"),
                    "category": props.get("categories")[0].split('.')[-1] if props.get("categories") else "Attraction",
                    "lat": props.get("lat"),
                    "lon": props.get("lon")
                })

        # 3. Validation: If API found nothing, use Fallback
        if len(places) < 5:
            return generate_fallback_places(destination)

        return places

    except Exception as e:
        print(f"Places API Error: {e}")
        return generate_fallback_places(destination)


def generate_fallback_places(destination: str):
    """
    Uses Groq to list famous places if the Real-Time API fails.
    """
    prompt = f"""
    List 10 famous tourist places in {destination}.
    Return ONLY a JSON object with a "places" key containing a list of strings.
    Example: {{ "places": ["Eiffel Tower", "Louvre Museum"] }}
    """

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "system", "content": "Return only valid JSON."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        # Cleaning Groq's output in case it adds markdown backticks
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
            
        return json.loads(content).get("places", [])
    except Exception:
        return []