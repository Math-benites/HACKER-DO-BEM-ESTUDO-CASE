import logging
import os
from logging.handlers import RotatingFileHandler

from flask import request


def _build_logger():
    log_dir = os.environ.get("TASK_MANAGER_LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("task_manager_audit")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = RotatingFileHandler(
            os.path.join(log_dir, "app.log"),
            maxBytes=1024 * 1024,
            backupCount=3,
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)

    return logger


audit_logger = _build_logger()


def audit_event(event, username="-", **extra):
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr or "-")
    if "," in ip_address:
        ip_address = ip_address.split(",", 1)[0].strip()

    fields = {
        "event": event,
        "username": username or "-",
        "ip": ip_address,
        "path": request.path,
        "method": request.method,
    }
    fields.update(extra)

    message = " ".join(f"{key}={value}" for key, value in fields.items())
    audit_logger.info(message)
