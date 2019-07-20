class Item:
    #all vars of item + who holds it
    def __init__(self, id, owner=0):
        #stats from items.csv and owner
        pass

    def use(self):
        #discard one use and launches cleanup
        pass

    def drop(self):
        #nobody holds it now...
        pass

    def pickup(self):
        #someone holds it now!
        pass

class Character:
    charlist=['nobody']
    def __init__(self, name, stats):
        pass

    def use(self, item_id):
        #launch item method
        pass

    def pickup(self, item_id, exists, drop):
        #create\update item
        #update weight and derived parameters
        pass
    
    def cleanup(self)
        #remove items with no charges
        pass