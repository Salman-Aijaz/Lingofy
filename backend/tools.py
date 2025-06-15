from langchain.prompts import PromptTemplate
from utils import clean_json_response
from state import AgentState
from llm import llm
from logger import logger

def translate_text(state: AgentState) -> AgentState:
    prompt = PromptTemplate.from_template("""
Translate the following paragraph into {lang} and return only the translated paragraph:
{paragraph}
""")
    lang_map = {"roman_urdu": "Roman Urdu", "croatian": "Croatian"}
    result = llm.invoke(prompt.format(
        lang=lang_map[state.language], paragraph=state.paragraph))
    state.translation = result.content.strip()
    logger.info("✅ Translation completed.")
    return state
    
def extract_difficult_words(state: AgentState) -> AgentState:
    prompt = PromptTemplate.from_template("""
Analyze the paragraph below and extract only those English words which are uncommon, complex, or rarely used in daily conversation.

Avoid extracting simple, familiar, or commonly known words that are widely understood by most English speakers.

Only return a JSON array (without any explanation or code block). If there are fewer than 10 difficult words, return only those that truly qualify.

Paragraph:
{paragraph}
""")
    result = llm.invoke(prompt.format(paragraph=state.paragraph))
    try:
        # Ensure we remove anything outside pure JSON
        words = clean_json_response(result.content)
    except Exception as e:
        logger.warning(
            f"⚠️ Failed to parse difficult words JSON: {e}\nRaw Output:\n{result.content}")
        words = []
    state.difficult_words = words
    logger.info(f"🔍 Extracted difficult words: {words}")
    return state

def fetch_meanings_synonyms(state: AgentState) -> AgentState:
    word_info = {}
    for word in state.difficult_words:
        prompt = PromptTemplate.from_template("""
Give 1 simple English meaning and 2 English synonyms for the word "{word}".

Respond ONLY with JSON (no explanation, no extra text), like:
{{
  "meaning": "simple definition here",
  "synonyms": ["synonym1", "synonym2"]
}}
""")
        result = llm.invoke(prompt.format(word=word))
        
        try:
            parsed = clean_json_response(result.content)
            if not parsed:
                parsed = {"meaning": "", "synonyms": []}
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to parse word info for '{word}': {e}\nRaw Output:\n{result.content}")
            parsed = {"meaning": "", "synonyms": []}
        word_info[word] = parsed
    state.word_info = word_info
    logger.info("📘 Fetched meanings and synonyms.")
    return state