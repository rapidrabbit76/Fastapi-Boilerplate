from optparse import Option
import os
import uuid
import logging
import json
from typing import Optional


from datetime import datetime
from json import JSONEncoder
from pythonjsonlogger import jsonlogger


class ModelJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class LogFilter(logging.Filter):
    def __init__(self, service=None, instance=None):
        self.service = service
        self.instance = instance

    def filter(self, record):
        record.service = self.service
        record.instance = self.instance
        return True


class JsonLogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            now = datetime.utcnow().isoformat()
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        if not log_record.get("type"):
            log_record["type"] = "internal"


def configure_logging(
    *,
    logging_path: str = "logs",
    logging_filename: str = "access.json",
    level: str = "DEBUG",
    service: Optional[str] = None,
    instance: Optional[str] = str(uuid.uuid4()),
    format: str = "%(timestamp)s %(level)s %(service)s %(instance)s %(type)s %(message)s",
    **kwargs,
):
    """
    kwargs:
        log_group_name: str = __name__,
        log_stream_name: str = DEFAULT_LOG_STREAM_NAME,
        use_queues: bool = True,
        send_interval: int = 60,
        max_batch_size: int = 1024 * 1024,
        max_batch_count: int = 10000,
        boto3_client: botocore.client.BaseClient = None,
        boto3_profile_name: str = None,
        create_log_group: bool = True,
        json_serialize_default: callable = None,
        log_group_retention_days: int = None,
        create_log_stream: bool = True,
        max_message_size: int = 256 * 1024,
        log_group=None,
        stream_name=None,
    """
    os.makedirs(logging_path, exist_ok=True)
    log_filename = os.path.join(logging_path, logging_filename)

    config = {
        "version": 1,
        "formatters": {
            "default": {
                "()": JsonLogFormatter,
                "format": format,
                "json_encoder": ModelJsonEncoder,
            }
        },
        "filters": {
            "default": {
                "()": LogFilter,
                "service": service,
                "instance": instance,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "filters": ["default"],
                "formatter": "default",
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_filename,
                "filters": ["default"],
                "formatter": "default",
                "maxBytes": 1024 * 1024 * 100,
                "backupCount": 5,
            },
        },
        "root": {
            "level": level,
            "handlers": ["console", "rotating_file"],
        },
    }
    logging.config.dictConfig(config)
