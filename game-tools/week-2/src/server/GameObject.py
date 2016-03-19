import json

class GameObject(object):
    def __init__(self, id, name, image, strength, defense, reliability):
        self._id = id
        self._name = name
        self._image = image
        self._strength = strength
        self._defense = defense
        self._reliability = reliability
        print("creating object %s with id %d image %s strength %d defense %d reliability %d" % (name, id, image, strength, defense, reliability))

    def fight(self, other):
        print("Object %s against %s" % (self._name, other._name))
        if other._strength > self._strength:
            print("loss 1")
            return -1
        if self._strength > (other._defense - self._reliability):
            print("win 1")
            return 1
        if other._defense > self._strength:
            print("loss 2")
            return -1
        print("tie 1")
        return 0

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getImage(self):
        return self._image

    def getStrength(self):
        return self._strength

    def getDefense(self):
        return self._defense

    def getReliability(self):
        return self._reliability

    def toJSON(self):
        return { 'id': self._id, 'name': self._name, 'image': self._image, 'strength': self._strength, 'defense': self._defense, 'reliability': self._reliability }

    def toString(self):
        print("object %s with id %d image %s strength %d defense %d reliability %d" % (self._name, self._id, self._image, self._strength, self._defense, self._reliability))
