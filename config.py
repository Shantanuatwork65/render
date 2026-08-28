import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    SECRET_KEY= os.getenv("SECRET_KEY", "default")
    DB_URL= os.getenv("DB_URL", "sqlite:///./test.db")
    ORIGIN=os.getenv("ORIGIN")
    CACHE_EXPIRATION= int(os.getenv("CACHE_EXPIRATION", 60))
    RATE_LIMIT= int(os.getenv("RATE_LIMIT", 5))

settings= Settings()