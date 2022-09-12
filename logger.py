import os
import logging

from config import get_settings

settings = get_settings()


class Logger:

    _formatter = logging.Formatter(
        '%(asctime)15s %(levelname)8s %(pathname)20s %(lineno)d || %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S'
    )

    def __init__(self):
        self.logger = logging.getLogger('sock')
        self.logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)

    def setup(self):
        self.logger.setLevel(logging.DEBUG)

        debug = logging.FileHandler(os.path.join(self.logs_dir, 'sock.debug'))
        debug.setLevel(logging.DEBUG)
        debug.setFormatter(self.formatter)

        warning = logging.StreamHandler()
        warning.setLevel(logging.INFO)
        warning.setFormatter(self.formatter)

        self.logger.addHandler(debug)
        self.logger.addHandler(warning)

        self.logger.info('tornado started')

    @property
    def formatter(self) -> logging.Formatter:
        return self._formatter


logger = Logger()
logger.setup()
