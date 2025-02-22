import logging.config

from src.configurations import defaults

logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})
logging.basicConfig(
    format="%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s",
    level=defaults.LOG_LEVEL
)
logger = logging.getLogger("main")