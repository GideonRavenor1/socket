from tornado.escape import json_encode


class ProjectData:

    def __init__(self):
        self.sockets = set()
        self.history = ''

    def hist_size(self):
        return len(self.history)

    def add_socket(self, sock):
        if sock not in self.sockets:
            self.sockets.add(sock)

    def process_mess(self, sock, mess):
        mess_type = mess['type']

        if mess_type == 'reg':
            return self._execute_req_mess_type(sock)

        if mess_type == 'history':
            self._execute_history_mess_type(sock=sock, mess=mess)

        self.broadcast_mess(sock, mess)

    def translate_data(self, data):
        for sock in self.sockets:
            sock.write_message(data)

    def remove_socket(self, sock):
        self.sockets.discard(sock)

        if len(self.sockets) == 0:
            self.history = ''

    def broadcast_mess(self, sock, mess):
        for sock_ in self.sockets:
            if sock_ != sock:
                sock_.write_message(mess)

    def clients_count(self):
        return len(self.sockets)

    def _execute_req_mess_type(self, sock):
        if len(self.history) != 0:
            sock.write_message(json_encode({"type": "history", "data": self.history}))
        else:
            sock.write_message(json_encode({"type": "history", "data": {"gHistory": [], "gHistoryUndoed": []}}))

    def _execute_history_mess_type(self, sock, mess):
        self.history = mess['data']
        sock.write_message(json_encode({"type": "history", "data": self.history}))