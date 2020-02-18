import numpy
from cave import *
import caveGui


def caveExample():
    myCollection = Collection()
    myCave = myCollection.createCave()
    print("Capacite:", myCave.getCapacite())
    print(myCave.id)

    v = myCollection.addVigneron("Alain Ducasse")
    b = Bottle("Chateau Ducasse", millesime=2010, vigneron=v)
    pos = Position(1, 1, 1, 1)
    print(myCollection.getVigneronName(b))

    myCollection.storeBottle(b, myCave, pos)
    myCollection.storeBottle(Bottle("Chateau Beauregard", millesime=2012), myCave, Position(1, 2, 1, 1))
    myCollection.storeBottle(Bottle("Chateau Beauregard", millesime=2012), myCave, Position(2, 1, 1, 1))
    myCollection.storeBottle(Bottle("Chateau Ducasse"   , millesime=2015), myCave, Position(2, 1, 1, 2))

    print("total bottles: ", myCollection.getTotalBottles())

    print("Remplissage: ", myCave.getRemplissage())

    d = myCollection.removeBottle(myCave, pos)

    print("Remplissage: ", myCave.getRemplissage())
    print("total bottles: ", myCollection.getTotalBottles())

    print("List Collection")
    myCollection.listBottles()

    # Save collection
    myCollection.saveCollection()

    # Load collection
    print("Reloaded")
    reloaded = Collection.loadCollection()
    reloaded.listBottles()
    return

def main():
    #caveExample()
    caveGui.CaveGUI().run()
    
if __name__ == "__main__":
  main()
