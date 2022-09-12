from websockets.base import BaseSocketHandler
from state import state


class ClientWsHandler(BaseSocketHandler):
    def open(self):
        self.log('Client connected')

    def process_message(self, message):
        data = message
        self.log('ON MESSAGE')
        self.log(data)
        pid = data['pid']
        mess_type = data['type']
        user_id = data['uid']

        if mess_type == 'reg':
            state.user_sockets.register(user_id, self)

        if pid not in state.projects_data:
            state.set_to_project_data(pid)

        state.get_from_projects_data(pid).add_socket(self)
        state.get_from_projects_data(pid).process_mess(self, message)

    def on_close(self):
        self.log('Closing Client')
        state.user_sockets.unregister(self)

        for _, project in state.projects_data.items():
            for socket in project.sockets:
                socket.log(socket.ws_connection)

            project.remove_socket(self)

        for proj_id, project in state.projects_data.items():
            if project.clients_count() == 0:
                state.delete_from_projects_data(proj_id)

        self.log('Client disconnected')

    def check_origin(self, origin):
        return True