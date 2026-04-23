from app.utils.places_data import PLACES_DB


def get_places(destination: str):
    destination = destination.lower()

    if destination in PLACES_DB:
        return PLACES_DB[destination]

    # fallback if city not in DB
    return [
        f"Famous place in {destination}",
        f"Top attraction in {destination}",
        f"Local market in {destination}",
        f"Popular tourist spot in {destination}"
    ]