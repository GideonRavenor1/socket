from .data import ProjectData
from websockets.user import UserSockets


class State:

    def __init__(self):
        self._projects_data = dict()
        self._runner_sockets = []
        self._tasks_socket = None
        self._user_sockets = UserSockets()

    @property
    def task_socket(self):
        return self._tasks_socket

    @task_socket.setter
    def task_socket(self, handler):
        self._tasks_socket = handler

    @property
    def user_sockets(self):
        return self._user_sockets

    @property
    def projects_data(self):
        return self._projects_data

    def set_to_project_data(self, pid):
        self._projects_data[pid] = ProjectData()

    def get_from_projects_data(self, pid, default=None):
        return self._projects_data.get(pid) or default

    def delete_from_projects_data(self, pid):
        del self._projects_data[pid]

    def add_runner_socket(self, handler):
        self._runner_sockets.append(handler)

    def delete_runner_socket(self, handler):
        self._runner_sockets.remove(handler)


state = State()
