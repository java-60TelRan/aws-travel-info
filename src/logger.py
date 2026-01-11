import logging
import os
def getLevelFromEnv(envName: str) -> int:
    level_name = os.getenv(envName, "INFO").upper()
    level = logging.getLevelName(level_name)

    if isinstance(level, str):
        return logging.INFO

    return level
    
logging.basicConfig(
    level=getLevelFromEnv("LOGGER_LEVEL"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("app")
logger.info(f"LOGGER LEVEL is {logger.getEffectiveLevel()}")