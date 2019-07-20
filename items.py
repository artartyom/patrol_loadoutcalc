class Item:

    def __init__(self, itemdata):
        self.name, self.type, self.weight, self.xpcost, self.maxcharges = itemdata
        self.weight = int(self.weight)
        self.xpcost = int(self.xpcost)
        self.maxcharges = int(self.maxcharges)
        self.currcharges = self.maxcharges

    def use(self):
        pass

def load_items(path_to_table):

    items = []

    with open(path_to_table) as datafile:
        line=datafile.readline()
        for line in datafile:
            items.append(line.strip('\n').split('\t')[1:])

    return items