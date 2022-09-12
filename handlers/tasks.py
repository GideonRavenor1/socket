import json

from websockets.base import BaseSocketHandler
from state import state


class TasksWsHandler(BaseSocketHandler):
    def open(self):
        state.tasks_socket = self
        self.log('Tasks connected')

    def process_message(self, message):
        params = message
        command = params.get('command', '')

        if command == 'task_status_changed':
            project = state.get_from_projects_data(params['project_id'])
            if not project:
                return

            project.broadcast_mess(self, json.dumps({
                'type': command,
                'pid': params['project_id'],
                'task_id': params['task_id'],
                'old_state': params['old_state'],
                'new_state': params['new_state'],
            }))
        elif command in ['task_added', 'task_deleted']:
            project = state.get_from_projects_data(params['project_id'])
            if not project:
                return

            project.broadcast_mess(self, json.dumps({
                'type': command,
                'pid': params['project_id'],
                'task_id': params['task_id']
            }))

    def on_close(self):
        self.log('Closing Tasks')
        state.tasks_socket = None
        self.log('Tasks disconnected')

    def check_origin(self, origin):
        return True