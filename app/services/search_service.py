# app/services/search_service.py
import requests
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def get_city_coordinates(destination: str):
    """
    Converts city name to lat/lon using Geoapify Geocoding API.
    """
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": destination,
        "format": "json",
        "apiKey": settings.GEOAPIFY_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results'):
            # Returning lat and lon of the most relevant result
            result = data['results'][0]
            return result['lat'], result['lon']
            
    except Exception as e:
        print(f"Geocoding Error: {e}")
        
    return None, None

def build_search_query(destination: str):
    """
    Kept your original logic for building queries if you still want 
    to use web search as an additional layer later.
    """
    prompt = f"Create a strong search query for tourist attractions in {destination}. Return ONLY the query string."
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()