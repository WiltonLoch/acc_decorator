class IntervalTree:
    def __init__(self, parent = None, start = None, end = None, level = 0):
        self.start = start
        self.end = end
        self.children = []
        self.parent = parent
        self.level = level

    def setIntervalStart(self, start):
        self.start = start

    def setIntervalEnd(self, end):
        self.end = end

    def getData(self):
        return [self.start, self.end]

    def getLevel(self):
        return self.level

    def addChild(self, Node):
        self.children.append(Node)

    def getChild(self, index):
        return self.children[index]

    def getChildren(self):
        return self.children

    def getChildrenNumber(self):
        return len(self.children)

    def getParent(self):
        return self.parent

    def traversePreOrder(self):
        for level in range(0, self.getLevel()):
            print("    ", end = '')
        print(self.getData())
        for child in self.getChildren():
            child.traversePreOrder()

    def getNodeNumber(self):
        total_descendants = self.getChildrenNumber()
        for child in self.getChildren():
            total_descendants += child.getNodeNumber()
        return total_descendants
