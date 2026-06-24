import logging
import sys
import colorlog


def setup_logging():
    handler = colorlog.StreamHandler(sys.stdout)

    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s"
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.handlers.clear()
    root_logger.addHandler(handler)