from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_CNXN_STRING")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")