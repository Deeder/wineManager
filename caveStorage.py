import numpy
import pickle

class Bottle:
    def __init__(self, name, cuvee=None, millesime=None, vigneronId=None):
        self.id         = id(self)
        self.name        = name
        self.cuvee      = cuvee
        self.millesime  = millesime
        self.vigneronId = vigneronId
        self.position   = None

    def getName(self):
        print(self.name)
        return self.name

    def setPosition(self, position):
        self.position = position

    def getDescription(self):
        pos = self.position.display() if self.position is not None else "()"
        s = "{0}, {1}, {2}, {3}".format(self.id, self.name, self.millesime, pos)
        return s


class Collection:
    def __init__(self):
        self.id    = id(self)
        self.caves = list()
        self.archive      = Storage()
        self.bottles_list = list()

    def createCave(self):
        c = Cave()
        self.caves.append(c)
        return c

    def addBottle(self, bottle):
        self.bottles_list.append(bottle)
        return

    def getTotalBottles(self):
        return len(self.bottles_list)
    
    def listBottles(self):
        for b in self.bottles_list:
            print(b.getDescription())

    def getBottleById(self, id):
        for b in self.bottles_list:
            if b.id == id:
                return b
        return None

    def storeBottle(self, bottle, cave, position):
        cave.storeBottle(bottle, position)
        self.addBottle(bottle)

    def removeBottle(self, cave, position):
        id = cave.removeBottle(position)
        bottle          = self.getBottleById(id)
        bottle.position = None
        return bottle


class Position:
    def __init__(self, shelf, z, y, x):
        self.shelf = shelf
        self.z = z
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.shelf == other.shelf) and (self.z == other.z) and (self.y == other.y) and (self.x == other.x)

    def display(self):
        return "({}, {}, {}, {})".format(self.shelf, self.z, self.y, self.x)


class Shelf:
    def __init__(self, id, depth, height, width):
        self.id = id
        self.height = height
        self.width  = width
        self.depth  = depth
        self.bottleIdList = list()
        self.positions    = list()

    def getCapacite(self):
        return self.height * self.width * self.depth

    def getBottlesNumbers(self):
        return len(self.bottleIdList)

    def addBottle(self, bottle, position):
        self.bottleIdList.append(bottle.id)
        self.positions   .append(position)
        bottle.setPosition(position)

    def getBottleByPosition(self, position):
        id = None
        for i, elt in enumerate(self.positions):
            if position == elt:
                id = i
        return self.bottleIdList[id], id

    def removeBottleByShelfID(self, id):
        position = self.positions[id]
        self.positions.pop(id)
        return self.bottleIdList.pop(id)

class Storage():
    def __init__(self):
        self.id         = id(self)
        self.shelves    = [Shelf(0, 0, 0, 0)]

    def getRemplissage(self):
        return sum([e.getBottlesNumbers() for e in self.shelves])

    def storeBottle(self, bottle, position):
        shelfId = position.shelf
        self.shelves[shelfId].addBottle(bottle, position)

    def removeBottle(self, position):
        shelfId = position.shelf
        id, bottleId_shelf = self.shelves[shelfId].getBottleByPosition(position)
        self.shelves[shelfId].removeBottleByShelfID(bottleId_shelf)
        return id


class Cave(Storage):
    def __init__(self, shelves=((1, 2, 5), (2, 3, 5), (2, 3, 5), (2, 3, 5))):
        super().__init__()
        self.shelves    = [Shelf(i, *x) for i, x in enumerate(shelves)]
        self.capacite   = sum([e.getCapacite() for e in self.shelves])
        
    def getCapacite(self):
        return self.capacite

    def getBottleByPosition(self, position):
        shelfId = position.shelf
        id, _   = self.shelves[shelfId].getBottleByPosition(position)
        return self.getBottleById(id)

def main():

    a = Collection()
    c = a.createCave()
    print("Capacite:", c.getCapacite())

    b = Bottle("Chateau Ducasse", millesime=2010)
    pos = Position(1, 1, 1, 1)

    a.storeBottle(b, c, pos)
    a.storeBottle(Bottle("Chateau Beauregard", millesime=2012), c, Position(1, 2, 1, 1))
    a.storeBottle(Bottle("Chateau Beauregard", millesime=2012), c, Position(2, 1, 1, 1))
    a.storeBottle(Bottle("Chateau Ducasse"   , millesime=2015), c, Position(2, 1, 1, 2))

    print("total bottles: ", a.getTotalBottles())

    print("Remplissage: ", c.getRemplissage())

    d = a.removeBottle(c, pos)

    print("Remplissage: ", c.getRemplissage())
    print("total bottles: ", a.getTotalBottles())

    print("List Collection")
    a.listBottles()

if __name__ == "__main__":
  main()
