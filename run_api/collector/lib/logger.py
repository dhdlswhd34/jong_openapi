import logging
import logging.config
import os

from lib.config import LoggerConfig

class Logger():
    @classmethod
    def get_logger(cls, filename='temp', name=None):
        conf_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = f'{LoggerConfig.path}/logs/{filename}'
        log_file = f'{log_path}/{filename}.log' if os.path.exists(log_path) else f'{log_path}.log'

        logging.config.fileConfig(f'{conf_dir}/logger.conf', defaults={'filename': log_file})
        return logging.getLogger(name)
