from socket import socket, SO_REUSEADDR, SOL_SOCKET
from asyncio import Task, coroutine, get_event_loop
import json

BASIC_CHANNEL = 'All'

class Peer(object):
    def __init__(self, server, sock, name):
        self.loop = server.loop
        self.name = name
        self.displayName = 'anonymous'
        self.channel = BASIC_CHANNEL
        self._sock = sock
        self._server = server
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

    @coroutine
    def _peer_loop(self):
        while True:
            buf = yield from self.loop.sock_recv(self._sock, 1024)
            if buf == b'':
                break
            data = json.loads(buf.decode())
            print('data received')
            print(data)
            if data['type'] == 1:
                self._server.broadcast(json.dumps({ 'type': 1, 'data': data['data'], 'from': self.displayName, 'channel': self.channel }), self.channel, self)
            if data['type'] == 2:
                self._server.broadcast(json.dumps({ 'type': 2, 'data': data['data'], 'from': self.displayName, 'channel': self.channel }), self.channel, self)
                self.displayName = data['data']
            if data['type'] == 3:
                self.channel = data['data']
                self._server.broadcast(json.dumps({ 'type': 3, 'data': '', 'from': self.displayName, 'channel': self.channel }), self.channel, self)

class Server(object):
    def __init__(self, loop, port):
        self.loop = loop
        self._serv_sock = socket()
        self._serv_sock.setblocking(0)
        self._serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serv_sock.bind(('',port))
        self._serv_sock.listen(5)
        print('Server listening on port ', port)
        self._peers = []
        Task(self._server())

    def remove(self, peer):
        self._peers.remove(peer)
        self.broadcast('Peer %s quit!\n' % (peer.displayName), peer.channel, peer)

    def broadcast(self, message, channel, sender):
        for peer in self._peers:
            if peer.channel == channel and peer != sender:
                peer.send(message)

    @coroutine
    def _server(self):
        while True:
            peer_sock, peer_name = yield from self.loop.sock_accept(self._serv_sock)
            peer_sock.setblocking(0)
            peer = Peer(self, peer_sock, peer_name)
            self._peers.append(peer)
            print('New Peer connected', peer_name)
            self.broadcast('Peer %s connected!\n' % (peer.displayName), peer.channel, peer)

def main():
    loop = get_event_loop()
    Server(loop, 5000)
    loop.run_forever()

if __name__ == '__main__':
    main()