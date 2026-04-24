# app/core/config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    # --- API Keys ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GEOAPIFY_API_KEY: str = os.getenv("GEOAPIFY_API_KEY")
    
    # --- Model Settings ---
    # Defaulting to llama-3.3-70b-versatile if not specified (fast and good for JSON)
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # --- App Logic Settings ---
    MEMORY_LIMIT: int = int(os.getenv("MEMORY_LIMIT", 10))

    def validate_keys(self):
        """Optional: Call this at startup to ensure you aren't missing critical keys."""
        missing = []
        if not self.GROQ_API_KEY: missing.append("GROQ_API_KEY")
        if not self.GEOAPIFY_API_KEY: missing.append("GEOAPIFY_API_KEY")
        
        if missing:
            print(f"⚠️ WARNING: Missing environment variables: {', '.join(missing)}")

# Create single instance of settings
settings = Settings()

# Basic validation check
settings.validate_keys()