import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    RESUME_PATH = "./curriculos/"
    APPROVED_PATH = "./aprovado/"
    REJECTED_PATH = "./recusado/"


settings = Settings()
