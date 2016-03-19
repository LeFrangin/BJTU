from socket import socket, SO_REUSEADDR, SOL_SOCKET
from asyncio import Task, coroutine
import xml.etree.ElementTree as etree
import json
import os
from GameObject import GameObject
from Peer import Peer
from UserState import UserState

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GameObject):
            return obj.toJSON()
        return json.JSONEncoder.default(self, obj)

class Server(object):
    def __init__(self, loop, port):
        self.loop = loop
        self._serv_sock = socket()
        self._serv_sock.setblocking(0)
        self._serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serv_sock.bind(('',port))
        self._serv_sock.listen(5)
        self._initFile = os.path.join(os.path.dirname(__file__), 'init.xml')
        self._tree = etree.parse(self._initFile)
        print('Server listening on port ', port)
        self._peers = []
        self._inRoom = []
        self._gameObjects = []
        self.getObjects()
        Task(self._server())

    def addToRoom(self, peer):
        if not peer in self._inRoom:
            self._inRoom.append(peer)
            peer.send(json.dumps({ 'state': 3 }))

    def removeFromRoom(self, peer, result=None):
        self._inRoom.remove(peer)
        peer.send(json.dumps({ 'state': 1, 'result': result }))

    def checkGame(self):
        loosers = []
        for player1 in self._inRoom:
            for player2 in self._inRoom:
                if player1 != player2:
                    result = player1.fight(player2)
                    if result == 1 and not (player2 in loosers):
                        self.removeFromRoom(player2, -1)
                        loosers.append(player2)
                        print('player2 loose with object ')
                        player2.getObject().toString()
                    elif result == -1 and not (player1 in loosers):
                        self.removeFromRoom(player1, -1)
                        loosers.append(player1)
                        print('player1 loose with object ')
                        player1.getObject().toString()
        winners = []
        for player in self._inRoom:
            if not (player in loosers):
                winners.append(player)
        if len(winners) == 1:
            self.removeFromRoom(winners[0], 1)
            for player in self._peers:
                player.emptyObject()
        else:
            for winner in winners:
                winner.send(json.dumps({ 'state': 3 }))

    def objectChosen(self, peer):
        found = False
        for peer in self._inRoom:
            if not peer.hasObject():
                found = True
                print('one has no object')
        if found or len(self._inRoom) == 1:
            print('sending wait')
            peer.send(json.dumps({ 'state': 4 }))
        else:
            print('checking game')
            self.checkGame()

    def remove(self, peer):
        self._peers.remove(peer)
        if peer in self._inRoom:
            self._inRoom.remove(peer)

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
            self.sendObjects(peer)

    def getObjects(self):
        root = self._tree.getroot()
        objects = root.find('objects').findall('object')
        for currentObject in objects:
            id = currentObject.attrib['id']
            name = currentObject.find('name').text
            image = currentObject.find('image').text
            strength = currentObject.attrib['strength']
            defense = currentObject.attrib['defense']
            reliability = currentObject.attrib['reliability']
            self._gameObjects.append(GameObject(int(id), name, image, int(strength), int(defense), int(reliability)))

    def sendObjects(self, peer):
        peer.send(json.dumps({ 'state': 5, 'objects': self._gameObjects }, cls=ComplexEncoder))

    def modifyObject(self, peer, objectId, newObject):
        root = self._tree.getroot()
        objects = root.find('objects').findall('object')
        for currentObject in objects:
            if int(currentObject.attrib['id']) == objectId:
                currentObject.find('name').text = newObject.getName()
                currentObject.find('image').text = newObject.getImage()
                currentObject.set('strength', str(newObject.getStrength()))
                currentObject.set('defense', str(newObject.getDefense()))
                currentObject.set('reliability', str(newObject.getReliability()))
                break
        self._tree.write(self._initFile)
        for currentObject in self._gameObjects:
            if currentObject.getId() == objectId:
                self._gameObjects[self._gameObjects.index(currentObject)] = newObject
        self.sendObjects(peer)

    def addObject(self, peer, newObject):
        search = True
        objectId = 1
        while search:
            lastId = objectId
            for currentObject in self._gameObjects:
                if currentObject.getId() == objectId:
                    objectId += 1
            if lastId == objectId:
                search = False
        newObject = GameObject(objectId, newObject['name'], newObject['image'], newObject['strength'], newObject['defense'], newObject['reliability'])
        self._gameObjects.append(newObject)
        objects = self._tree.getroot().find('objects')
        newElement = etree.Element('object', { 'id': str(objectId), 'strength': str(newObject.getStrength()), 'defense': str(newObject.getDefense()), 'reliability': str(newObject.getReliability()) })
        newElementName = etree.Element('name')
        newElementName.text = newObject.getName()
        newElementImage = etree.Element('image')
        newElementImage.text = newObject.getImage()
        newElement.append(newElementName)
        newElement.append(newElementImage)
        objects.append(newElement)
        self._tree.write(self._initFile)
        self.sendObjects(peer)

    def removeObject(self, peer, objectId):
        for currentObject in self._gameObjects:
            if currentObject.getId() == objectId:
                self._gameObjects.remove(currentObject)
                break
        objects = self._tree.getroot().find('objects')
        objectList = objects.findall('object')
        for currentObject in objectList:
            if int(currentObject.attrib['id']) == objectId:
                objects.remove(currentObject)
                break
        self._tree.write(self._initFile)
        self.sendObjects(peer)

    def getObject(self, id):
        for gameObject in self._gameObjects:
            if gameObject.getId() == id:
                return gameObject
        return None