def estimate_budget(destination: str, days: int, budget_type: str):
    base_cost = {
        "low": 1000,
        "medium": 3000,
        "luxury": 8000
    }

    daily = base_cost.get(budget_type.lower(), 3000)

    total = daily * days

    return {
        "destination": destination,
        "days": days,
        "budget_type": budget_type,
        "estimated_cost": f"{total} INR"
    }