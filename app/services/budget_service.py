# app/services/budget_service.py
import requests
from app.core.config import settings

def fetch_live_budget_data(destination: str):
    """
    Fetches real hotel price data from TripAdvisor via RapidAPI.
    """
    # Step 1: Search for the city's Location ID
    search_url = "https://travel-advisor.p.rapidapi.com/locations/search"
    
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }
    
    try:
        search_params = {"query": destination, "units": "km"}
        response = requests.get(search_url, headers=headers, params=search_params)
        response.raise_for_status()
        data = response.json()
        
        # Get the ID of the first result
        location_results = data.get('data', [])
        if not location_results:
            return None
            
        location_id = location_results[0].get('result_object', {}).get('location_id')
        
        if not location_id:
            return None

        # Step 2: Get Hotels in that location to find the average price
        hotel_url = "https://travel-advisor.p.rapidapi.com/hotels/list"
        hotel_params = {
            "location_id": location_id,
            "currency": "USD",
            "limit": "10"
        }
        
        hotel_res = requests.get(hotel_url, headers=headers, params=hotel_params)
        hotel_res.raise_for_status()
        hotel_data = hotel_res.json().get('data', [])
        
        prices = []
        for hotel in hotel_data:
            price_str = hotel.get('price') # Format: "$120 - $200"
            if price_str and "$" in price_str:
                # Get the first number found in the string
                clean_price = "".join(filter(str.isdigit, price_str.split('-')[0]))
                if clean_price:
                    prices.append(float(clean_price))
        
        if prices:
            return round(sum(prices) / len(prices), 2)
            
    except Exception as e:
        print(f"⚠️ Budget API Error: {e}")
    
    return None

def estimate_budget(destination: str, days: int, budget_level: str):
    """
    Combines live data with logic to create a full trip estimate.
    """
    avg_hotel_price = fetch_live_budget_data(destination) or 100.0
    
    # Scale based on user preference
    multipliers = {"budget": 0.6, "medium": 1.0, "luxury": 2.5}
    m = multipliers.get(budget_level.lower(), 1.0)
    
    selected_hotel_price = avg_hotel_price * m
    daily_living_cost = selected_hotel_price * 0.5 # Food/Transport
    
    total_cost = (selected_hotel_price + daily_living_cost) * days
    
    return {
        "daily_hotel": round(selected_hotel_price, 2),
        "daily_allowance": round(daily_living_cost, 2),
        "total_cost": round(total_cost, 2),
        "currency": "USD"
    }