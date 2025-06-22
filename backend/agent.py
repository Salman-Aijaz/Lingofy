# agent.py
from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.tools import translate_text ,extract_difficult_words,fetch_meanings_synonyms

# --- LangGraph Agent ---

def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("translate", translate_text)
    workflow.add_node("extract", extract_difficult_words)
    workflow.add_node("meaning", fetch_meanings_synonyms)

    workflow.set_entry_point("translate")
    workflow.add_edge("translate", "extract")
    workflow.add_edge("extract", "meaning")
    workflow.add_edge("meaning", END)

    return workflow.compile()
