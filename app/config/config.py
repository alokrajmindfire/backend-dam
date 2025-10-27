import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
