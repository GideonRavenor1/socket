from tornado.escape import json_encode

from state import state
from websockets.base import BaseSocketHandler


class RunnerWsHandler(BaseSocketHandler):
    def open(self):
        state.add_runner_socket(self)
        self.log('Runner connected')

    def process_message(self, message):
        command = message.get('command', '')

        if command in ['stop_task_state']:
            if not state.tasks_socket:
                return

            state.tasks_socket.write_message(json_encode(message))

    def on_close(self):
        self.log('Closing Runner')
        state.delete_runner_socket(self)
        self.log('Runner disconnected')

    def check_origin(self, origin):
        return True
