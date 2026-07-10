from flask import request
from core_bank.utils.logger import setup_logger

logger = setup_logger()


def audit_log(message):

    ip = request.remote_addr

    logger.info(f"{ip} | {message}")
