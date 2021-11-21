import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


class Logger:
    def __init__(self, name: str, log_level: str = LOG_LEVEL):
        self.name = name
        self.log_level = logging.getLevelName(LOG_LEVEL)
        logging.basicConfig(
            handlers=[
                logging.StreamHandler()
            ],
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG
        )
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)
