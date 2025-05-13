import sys
from pathlib import Path
from time import time

from loguru import logger
from pathlib import Path

from pyexsys.consts.env import PYEXSYS_LOG_PATH


class ExpertSystemClassifyLogger:

    def __init__(self, output_dir: Path, log_level: str = 'DEBUG'):

        # log_level = "DEBUG" if verbose else "INFO"
        log_path = (
            Path(PYEXSYS_LOG_PATH).resolve()
            if PYEXSYS_LOG_PATH else output_dir.resolve() / "logs" / "expert_system_classify_{time}.log"
        )
        if not log_path.suffix:
            raise Exception(f'log path "{log_path}" not a file')

        logger.remove()

        logger.add(
            sys.stdout, colorize=True, level=log_level,
            format="[<green>{time}</green>] <level>{level: <8}</level>    - {message}"
        )

        logger.add(
            str(log_path), colorize=False, level=log_level,
            format="[<green>{time}</green>] <level>{level: <8}</level>    - {message}"
        )

        logger.info('Expert System Classify Starting...')

        self.log_level = log_level
        self.logger = logger

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)


pyexsys_logger = ExpertSystemClassifyLogger(output_dir=Path('.'))
