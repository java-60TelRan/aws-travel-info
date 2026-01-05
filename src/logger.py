import logging
import os
logger = logging.getLogger("app")
levelName: str = os.getenv("LOGGER_LEVEL", "INFO")
level: int = logging._nameToLevel.get(levelName, logging.INFO)
logger.setLevel(level)