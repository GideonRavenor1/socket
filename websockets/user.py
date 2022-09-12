class UserSockets:
    __user_sockets = dict()

    def register(self, user_id, socket):
        if user_id not in self.__user_sockets:
            self.__user_sockets[user_id] = list()
        self.__user_sockets[user_id].append(socket)

    def unregister(self, socket):
        for user_id, sockets in self.__user_sockets.items():
            if socket not in sockets:
                continue

            sockets.remove(socket)
            if not sockets:
                del self.__user_sockets[user_id]

            break

    def is_registered(self, user_id):
        return user_id in self.__user_sockets

    def send_message_to_user(self, user_id, message):
        if not self.is_registered(user_id):
            return

        sockets = self.__user_sockets[user_id]
        for socket in sockets:
            socket.write_message(message)
