# state.py
from pydantic import BaseModel
from typing import Literal, List, Dict

class AgentState(BaseModel):
    paragraph: str
    language: Literal["roman_urdu", "croatian"]
    translation: str = ""
    difficult_words: List[str] = []
    word_info: Dict[str, Dict[str, object]] = {}


class ParagraphInput(BaseModel):
    paragraph: str
    language: str  # 'roman_urdu' or 'croatian'
