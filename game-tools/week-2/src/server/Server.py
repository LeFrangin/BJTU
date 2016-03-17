from socket import socket, SO_REUSEADDR, SOL_SOCKET
from asyncio import Task, coroutine
import xml.etree.ElementTree as etree
import json
from GameObject import GameObject
from Peer import Peer
from UserState import UserState

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
        self._gameObjects = []
        self.getObjects()
        Task(self._server())

    def remove(self, peer):
        self._peers.remove(peer)

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

    def getObjects(self):
        root = etree.parse('init.xml').getroot()
        objects = root.find('objects').findall('object')
        for currentObject in objects:
            id = currentObject.attrib['id']
            name = currentObject.find('name').text
            image = currentObject.find('image').text
            strength = currentObject.attrib['strength']
            defense = currentObject.attrib['defense']
            reliability = currentObject.attrib['reliability']
            self._gameObjects.append(GameObject(int(id), name, image, int(strength), int(defense), int(reliability)))