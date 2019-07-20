import windows

class Owner:

    def __init__(self, itemlist=[]):
        self.itemlist = itemlist    

    def additem(self, item_id):
        self.itemlist.append(items[item_id])


class OwnerData:
    
    global owners
    global items

    def __init__(self, ownerName, itemlist=[]):
        self.name = ownerName
        self.info = Owner(itemlist)
        self.window = windows.Window(ownerName)
        owners[self.name]=self

    def additem(self, item_id)
        item_data = getitem(item_id)
        self.info.additem(item_id)

    def refresh(self)
