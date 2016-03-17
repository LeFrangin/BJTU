import json

class GameObject(object):
    def __init__(self, id, name, image, strength, defense, reliability):
        self._id = id
        self._name = name
        self._image = image
        self._strengh = strength
        self._defense = defense
        self._reliability = reliability
        print("creating object %s with id %d image %s strength %d defense %d reliability %d" % (name, id, image, strength, defense, reliability))

    def fight(self, other):
        if other._strengh > self._strength:
            return -1
        if self._strength > (other._defense - self._reliability):
            return 1
        if other._defense > self._strength:
            return -1
        return 0


    def toJSON(self):
        return json.dumps({ 'id': self._id, 'name': self._name, 'image': self._image, 'strength': self._strengh, 'defense': self._defense, 'reliability': self._reliability })
