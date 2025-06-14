# utils.py

import json
import logging

logger = logging.getLogger(__name__)

def clean_json_response(raw_response: str) -> dict | list:
    """
    Cleans and parses LLM output to return valid JSON.
    """
    raw = raw_response.strip()

    # Remove code block formatting if exists
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"⚠️ Failed to parse JSON:\n{raw_response}\nError: {e}")
        return {} if '{' in raw else []
