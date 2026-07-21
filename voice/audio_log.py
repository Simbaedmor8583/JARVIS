"""Centralized audio logger -> %LOCALAPPDATA%\\JARVIS\\logs\\audio.log.

Every audio stage writes here with a timestamp and never swallows
exceptions; tracebacks are logged in full.
"""
import logging
import traceback

from config import Config

_logger = None


def get_audio_logger():
    global _logger
    if _logger is not None:
        return _logger
    logger = logging.getLogger("jarvis.audio")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if not logger.handlers:
        try:
            Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(
                Config.LOG_DIR / "audio.log", mode="a", encoding="utf-8"
            )
            handler.setFormatter(
                logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
            )
            logger.addHandler(handler)
        except Exception:
            logger.addHandler(logging.NullHandler())
    _logger = logger
    return logger


def log(message):
    get_audio_logger().info(message)


def log_error(message, exc=None):
    logger = get_audio_logger()
    logger.error(message)
    if exc is not None:
        logger.error("".join(traceback.format_exception(
            type(exc), exc, exc.__traceback__)))