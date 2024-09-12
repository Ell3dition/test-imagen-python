import logging
import os
from logging.config import dictConfig

from app.core.constants import PROJECT_NAME

if not os.path.isdir("./logs"):
    os.mkdir("./logs")


LOG_FORMAT: str = (
    '{"time": "%(asctime)s", "level": "%(levelname)s", '
    + '"thread": "%(threadName)s", "component": "%(module)s",'
    + f'"service": "{PROJECT_NAME}", "payload": %(message)s}}'
)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "class": "logging.Formatter",
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": logging.INFO,
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": logging.INFO,
            "filename": f"./logs/{PROJECT_NAME}.log",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 5000000,
            "backupCount": 4,
        },
        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "level": logging.DEBUG,
            "filename": f"./logs/{PROJECT_NAME}_debug.log",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 5000000,
            "backupCount": 4,
        },
    },
    "loggers": {
        PROJECT_NAME: {
            "handlers": ["console", "file", "debug_file"],
            "level": logging.DEBUG,
            "propagate": False,
        },
    },
}


def create_logger(
    config: dict = LOG_CONFIG,
) -> logging.Logger:
    dictConfig(config)
    return logging.getLogger(PROJECT_NAME)
