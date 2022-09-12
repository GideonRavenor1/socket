from tornado.escape import json_encode

from services.state import state
from websockets.base import BaseSocketHandler


class TasksWsHandler(BaseSocketHandler):
    def open(self):
        state.tasks_socket = self
        self.log('Tasks connected')

    def process_message(self, message):
        command = message.get('command', '')

        if not command:
            return

        project = state.get_from_projects_data(message['project_id'])
        if not project:
            return

        command = f'_handle_{command}'
        if hasattr(self, command):
            getattr(self, command)(project, command, message)

    def on_close(self):
        self.log('Closing Tasks')
        state.tasks_socket = None
        self.log('Tasks disconnected')

    def check_origin(self, origin):
        return True

    def _handle_task_added(self, project, command, params):
        self._broadcast_mess(
            project=project, params={
                'type': command,
                'pid': params['project_id'],
                'task_id': params['task_id']
            }
        )

    def _handle_task_deleted(self, project, command, params):
        self._broadcast_mess(
            project=project, params={
                'type': command,
                'pid': params['project_id'],
                'task_id': params['task_id']
            }
        )

    def _handle_task_status_changed(self, project, command, params):
        self._broadcast_mess(
            project=project, params={
                'type': command,
                'pid': params['project_id'],
                'task_id': params['task_id'],
                'old_state': params['old_state'],
                'new_state': params['new_state'],
            }
        )

    def _broadcast_mess(self, project, params):
        project.broadcast_mess(self, json_encode(params))