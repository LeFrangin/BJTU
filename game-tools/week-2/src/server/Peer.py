from asyncio import Task, coroutine
import json
from UserState import UserState
from GameObject import GameObject

class Peer(object):
    def __init__(self, server, sock, name):
        self.loop = server.loop
        self._state = UserState.pending
        self._sock = sock
        self._server = server
        self._actions = [self.actionPending, self.actionPlaying, self.actionChoosing, self.actionEditObject]
        self._object = None
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
        self._object = None
        self._state = UserState.pending
        self._server.removeFromRoom(self)

    def actionPlaying(self, data):
        self._object = None
        self._state = UserState.playing
        self._server.addToRoom(self)

    def actionChoosing(self, data):
        print('in action choosing')
        self._object = self._server.getObject(data["id"])
        if self._object == None:
            print('object not found')
            self.actionPending()
        print('object found')
        self._object.toString()
        self._state = UserState.waiting
        self._server.objectChosen(self)

    def actionEditObject(self, data):
        self._server.modifyObject(self, data["id"], GameObject(data["id"], data["name"], data["image"], data["strength"], data["defense"], data["reliaility"]))

    def getState(self):
        return self._state

    def hasObject(self):
        return self._object != None

    def getObject(self):
        return self._object

    def emptyObject(self):
        self._object = None

    def fight(self, other):
        return self.getObject().fight(other.getObject())

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