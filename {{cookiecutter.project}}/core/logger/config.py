import logging
import sys
from pprint import pformat

# if you dont like imports of private modules
# you can move it to typing.py module
from loguru import logger
from loguru._defaults import LOGURU_FORMAT, env
from .handler import InterceptHandler
import json


def format_record(record: dict) -> str:
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def sink_serializer(message):
    record = message.record
    simplified = {
        "level": record["level"].name,
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "message": record["message"],
    }
    serialized = json.dumps(simplified)
    print(serialized, file=sys.stderr)


def init_logging():
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [
        InterceptHandler(),
    ]

    # set logs output, level and format
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.DEBUG,
                "format": format_record,
            },
            # {
            #     "sink": sink_serializer,
            #     "level": logging.INFO,
            #     "format": "{level}: {time} [{name}] {message}",
            # },
        ]
    )
