import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL")

    MEMORY_LIMIT: int = int(os.getenv("MEMORY_LIMIT", 10))


settings = Settings()