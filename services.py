import json


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
        data = mess
        mess_type = data['type']

        if mess_type == 'reg':
            if len(self.history) != 0:
                sock.write_message('{"type":"history", "data":' + json.dumps(self.history) + '}')
            else:
                sock.write_message('{"type":"history", "data":{"gHistory": [], "gHistoryUndoed": []}}')
            return

        elif mess_type == 'history':
            self.history = data['data']
            sock.write_message('{"type":"history", "data":' + json.dumps(self.history) + '}')

        self.broadcast_mess(sock, mess)

    def translate_data(self, data):
        for sock in self.sockets:
            sock.write_message(data)

    def remove_socket(self, sock):
        self.sockets.discard(sock)

        if len(self.sockets) == 0:
            self.history = ''

    def broadcast_mess(self, sock, mess):
        for xsock in self.sockets:
            if xsock != sock:
                xsock.write_message(mess)

    def clients_count(self):
        return len(self.sockets)
