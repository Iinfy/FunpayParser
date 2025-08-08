import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="WARNING")
logger.add("logs/log_{time:YYYY-MM-DD}.log",level="DEBUG",rotation="1 day",format="{time} | {level} | {module} | {function} | {message}")

log = logger