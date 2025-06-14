# logger.py
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("✅ Logger initialized successfully.")

logger = logging.getLogger(__name__)
