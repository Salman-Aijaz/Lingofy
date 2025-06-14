import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Gemini Model ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # or use "gemini-2.0-flash" if needed
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY
)
