from fastapi import FastAPI
from backend.agent import build_agent
from dotenv import load_dotenv
import os
from backend.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from backend.state import ParagraphInput

# --- Load .env ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- LangGraph agent ---
agent = build_agent()

# --- Log API Key Check ---
if GOOGLE_API_KEY:
    logger.info("✅ Google Gemini API key loaded from .env.")
else:
    logger.warning("⚠️ Google Gemini API key NOT found! Please check your .env file.")


# --- FastAPI App ---
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://lingofy.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check Route ---
@app.get("/ping")
def ping():
    logger.info("🟢 Ping received")
    return {"message": "pong"}

@app.post("/process/")
def process_text(data: ParagraphInput):
    logger.info(f"📝 Received paragraph. Language: {data.language}")
    
    if len(data.paragraph.split()) > 200:
        return {"error": "Paragraph exceeds 200 word limit."}

    state = agent.invoke({
        "paragraph": data.paragraph,
        "language": data.language,
    })

    return {
        "translation": state["translation"],
        "difficult_words": state["difficult_words"],
        "word_info": state["word_info"]
    }
