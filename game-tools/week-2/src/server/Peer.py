from asyncio import Task, coroutine
import json
from UserState import UserState

class Peer(object):
    def __init__(self, server, sock, name):
        self.loop = server.loop
        self._state = UserState.pending
        self._sock = sock
        self._server = server
        self._actions = [self.actionPending, self.actionPlaying, self.actionChoosing]
        Task(self._peer_handler())

    def send(self, data):
        return self.loop.sock_sendall(self._sock, data.encode('utf8'))
    
    @coroutine
    def _peer_handler(self):
        try:
            yield from self._peer_loop()
        except IOError:
            pass
        finally:
            self._server.remove(self)

    def actionPending(self, data):
        print('1')

    def actionPlaying(self, data):
        print('1')

    def actionChoosing(self, data):
        print('1')

    @coroutine
    def _peer_loop(self):
        while True:
            buf = yield from self.loop.sock_recv(self._sock, 1024)
            if buf == b'':
                break
            data = json.loads(buf.decode())
            print('data received')
            print(data)
            self._actions[int(data["state"]) - 1](data)
#            if data['type'] == 1:
#                self._server.broadcast(json.dumps({ 'type': 1, 'data': data['data'], 'from': self.displayName, 'channel': self.channel }), self.channel, self)