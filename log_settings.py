from loguru import logger
import os, sys


os.makedirs('logs', exist_ok=True)

logger.remove()

logger.add(sys.stdout,
           colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",)

logger.add('logs/actions.log',
           rotation="5 MB",
           compression="zip",
           level="INFO",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")