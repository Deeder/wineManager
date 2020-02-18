import pickle

class Collection:
    def __init__(self):
        self.id    = id(self)
        self.caves = list()
        self.archive      = Storage()
        self.bottles_list = list()
        self.vignerons    = VigneronsList()

    def createCave(self):
        c = Cave()
        self.caves.append(c)
        return c

    def addBottle(self, bottle):
        self.bottles_list.append(bottle)
        return

    def addVigneron(self, name):
        v = self.vignerons.addVigneron(name)
        return v

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

    def getVigneronById(self, id):
        return self.vignerons.getVigneronById(id)

    def getVigneronName(self, bottle):
        return self.vignerons.getVigneronById(bottle.vigneronId).name

    def storeBottle(self, bottle, cave, position):
        cave.storeBottle(bottle, position)
        self.addBottle(bottle)

    def removeBottle(self, cave, position):
        id = cave.removeBottle(position)
        bottle          = self.getBottleById(id)
        bottle.position = None
        return bottle

    def saveCollection(self, fileName="collection.data"):
        with open(fileName, 'wb') as f:
            pickle.dump(self, f)
    @classmethod
    def loadCollection(cls, fileName="collection.data"):
        with open(fileName, 'rb') as f:
            return pickle.load(f)

class Storage():
    def __init__(self):
        self.id         = id(self)
        self.shelves    = [Shelf(0, 0, 0, 0)]

    def getRemplissage(self):
        return sum([e.getBottlesNumbers() for e in self.shelves])

    def storeBottle(self, bottle, position):
        shelfId = position.shelfId
        self.shelves[shelfId].addBottle(bottle, position)

    def removeBottle(self, position):
        shelfId = position.shelfId
        id, bottleId_shelf = self.shelves[shelfId].getBottleByPosition(position)
        self.shelves[shelfId].removeBottleByShelfID(bottleId_shelf)
        return id

class Cave(Storage):
    # Shelves size are specified in (depth, height and width).
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

    def getCaveId(self):
        return self.id

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

class Bottle:
    def __init__(self, name, cuvee=None, millesime=None, vigneron=None, price=None):
        self.id         = id(self)
        self.name       = name
        self.cuvee      = cuvee
        self.millesime  = millesime
        self.vigneronId = vigneron.id if vigneron is not None else None
        self.position   = None
        self.price      = price

    def getName(self):
        print(self.name)
        return self.name

    def setPosition(self, position):
        self.position = position

    def getDescription(self):
        pos = self.position.display() if self.position is not None else "()"
        s = "{0}, {1}, {2}, {3}, {4}".format(self.id, self.name, self.millesime, pos, self.vigneronId)
        return s


class Position:
    def __init__(self, shelfId, z, y, x):
        self.shelfId = shelfId
        self.z = z
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.shelfId == other.shelfId) and (self.z == other.z) and (self.y == other.y) and (self.x == other.x)

    def display(self):
        return "({}, {}, {}, {})".format(self.shelfId, self.z, self.y, self.x)


class VigneronsList:
    def __init__(self):
        self.vignerons = list()

    def addVigneron(self, name, location=None):
        # Check for existing vigneron
        for v in self.vignerons:
            if v.name == name:
                return v
        # Else create a new one
        v = Vigneron(name, location)
        self.vignerons.append(v)
        return v

    def getVigneronById(self, id):
        for v in self.vignerons:
            if v.id == id:
                return v
        return None

    def getVigneronByName(self, name):
        for v in self.vignerons:
            if v.name == name:
                return v
        return None

class Vigneron:
    def __init__(self, name, location=None):
        self.id   = id(self)
        self.name = name
        self.location = location