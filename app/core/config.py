# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GEOAPIFY_API_KEY: str = os.getenv("GEOAPIFY_API_KEY")
    RAPIDAPI_KEY: str = os.getenv("RAPIDAPI_KEY")  # Added this line
    
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    MEMORY_LIMIT: int = int(os.getenv("MEMORY_LIMIT", 10))

settings = Settings()