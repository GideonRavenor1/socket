from tornado.escape import json_decode
from tornado.websocket import WebSocketHandler

from logger import logger


class BaseSocketHandler(WebSocketHandler):

    def write_message(self, data, **kwargs):
        try:
            super().write_message(data)
        except Exception as exc:
            logger.exception(f'Unable to write data to socket ({id(self)}): {exc}')

    def log(self, message):
        logger.debug(f'[Socket {id(self)}] {message}')

    def on_message(self, message):
        try:
            self.process_message(json_decode(message))
        except Exception as exc:
            logger.exception(f'Unable to process message from socket ({id(self)}): {exc}')
            logger.debug(message)

    def process_message(self, message):
        raise NotImplementedError()