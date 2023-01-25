import re

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

def insertDecorations(code, node, offset_lines = 0):
    insert_string = ""
    if ( node.get_data()[0] != None ):
        if (len( node.get_children()) == 0 and node.get_level() == 1 ):
            code.insert(node.get_data()[0] + offset_lines, loop_directives[0 + node.get_level() - 1] + ' VECTOR\n')
        else:
            code.insert(node.get_data()[0] + offset_lines, loop_directives[0 + node.get_level() - 1] + '\n')
        offset_lines += 1

    for child in node.get_children():
        offset_lines = insertDecorations(code, child, offset_lines)

    if( node.get_data()[0] != None ):
        code.insert(node.get_data()[1] + offset_lines + 1, end_loop_directives[0 + node.get_level() > 1] + '\n')
        offset_lines += 1

    return offset_lines

with open("input_code.F90", "r") as input_file:
    code = input_file.readlines()

loop_directives = ["!$ACC PARALLEL LOOP GANG", "!$ACC LOOP VECTOR", "!$ACC LOOP SEQ"]
end_loop_directives = ["!$ACC END PARALLEL LOOP", "!$ACC END LOOP"]

root = IntervalTree()
current_tree = root

for i in range(0, len(code)):
    line = code[i]
    if( re.search("^ *do .*", line) ):
        new_tree = IntervalTree(current_tree, i, -1, current_tree.get_level() + 1)
        current_tree.add_child(new_tree)
        current_tree = new_tree
    elif( re.search(".*end.*do.*", line) ):
        current_tree.set_end(i)
        current_tree = current_tree.get_parent()

insertDecorations(code, root)

with open("output_code.F90", "w") as output_file:
    output_file.writelines(code)
