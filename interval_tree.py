class IntervalTree:
    def __init__(self, parent = None, start = None, end = None, level = 0):
        self.start = start
        self.end = end
        self.children = []
        self.parent = parent
        self.level = level

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def get_data(self):
        return [self.start, self.end]

    def get_level(self):
        return self.level

    def add_child(self, Node):
        self.children.append(Node)

    def get_child(self, index):
        return self.children[index]

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

def traversePreOrder(node):
    print(node.get_data())
    for child in node.get_children():
        for level in range(0, child.get_level()):
            print("    ", end = '')
        traversePreOrder(child)
