import sys

from loguru import logger

from src.config.config import get_settings


def configure_logging():
    settings = get_settings()

    logger.remove()

    level = "DEBUG" if settings.debug else "INFO"

    if settings.log_format == "json":
        fmt = "{time:YYYY-MM-DDTHH:mm:ssZ} | {level} | {name}:{function}:{line} | {message}"
        logger.add(sys.stdout, format=fmt, level=level, serialize=True)
    else:
        fmt = "<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
        logger.add(sys.stdout, format=fmt, level=level, colorize=True)
