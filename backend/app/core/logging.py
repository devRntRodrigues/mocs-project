import sys

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.app.debug else "INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    if not settings.app.debug:
        logger.add(
            "logs/app_{time:YYYY-MM-DD}.log",
            format=log_format,
            level="INFO",
            rotation="1 day",
            retention="30 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
        )

    logger.info("Successfully configured logging")


configure_logging()
