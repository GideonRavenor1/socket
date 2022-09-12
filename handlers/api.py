from tornado.escape import json_encode, recursive_unicode
from tornado.web import RequestHandler

from state import state


class ApiHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, param):
        method = f'_handle_{param}'
        if hasattr(self, method):
            getattr(self, method)()

    def _handle_results(self):
        project_id = self.get_arguments('project_id')
        if not project_id:
            return

        pid = int(project_id[0])
        if pid not in state.projects_data:
            return

        state.get_from_projects_data(pid).translate_data(json_encode(recursive_unicode(self.request.arguments)))

    def _handle_notification_to_user(self):
        user_ids = self.get_arguments('user_ids')
        message = self.get_arguments('messages')
        for user_id in user_ids:
            state.user_sockets.send_message_to_user(int(user_id), message[0])

    def _handle_current_projects(self):
        self.write(json_encode(list(state.projects_data.keys())))

    def _handle_is_user_connected(self):
        user_id = self.get_arguments('user_id')[0]
        connected = state.user_sockets.is_registered(user_id)
        self.write(
            json_encode(
                {
                    'user_id': user_id,
                    'connected': connected,
                }
            )
        )

    def _handle_ping(self):
        self.write('ok')