from tornado.escape import json_encode


class UserSockets:
    __user_sockets = dict()

    def register(self, user_id, socket):
        if user_id not in self.__user_sockets:
            self._set_socket(user_id)
        self._get_socket_by_id(user_id).append(socket)

    def unregister(self, socket):
        for user_id, sockets in self._get_sockets().items():
            if socket not in sockets:
                continue

            sockets.remove(socket)
            if not sockets:
                self._delete_socket(user_id)

            break

    def is_registered(self, user_id):
        return user_id in self.__user_sockets

    def send_message_to_user(self, user_id, message):
        if not self.is_registered(user_id):
            return

        sockets = self._get_socket_by_id(user_id)
        for socket in sockets:
            socket.write_message(json_encode(message))

    def _delete_socket(self, user_id):
        del self.__user_sockets[user_id]

    def _get_sockets(self):
        return self.__user_sockets

    def _get_socket_by_id(self, user_id):
        return self.__user_sockets[user_id]

    def _set_socket(self, user_id):
        self.__user_sockets[user_id] = list()
