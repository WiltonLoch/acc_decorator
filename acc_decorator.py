import re
from interval_tree import IntervalTree

def insertDecorations(code, node, offset_lines = 0):
    insert_string = "\n"
    if ( node.getData()[0] != None ):
        if ( node.getLevel() == 1 ):
            if ( len( node.getChildren()) == 0 ):
                insert_string = " VECTOR PRIVATE() IF(.false.)\n"
            else:
                insert_string = " PRIVATE() IF(.false.)\n"
        code.insert(node.getData()[0] + offset_lines, loop_directives[node.getLevel() - 1] + insert_string)
        offset_lines += 1

    for child in node.getChildren():
        offset_lines = insertDecorations(code, child, offset_lines)

    if( node.getData()[0] != None ):
        code.insert(node.getData()[1] + offset_lines + 1, end_loop_directives[node.getLevel() > 1] + '\n')
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
    if( re.search("^ *[d,D][o,O] .*", line) ):
        new_tree = IntervalTree(current_tree, i, -1, current_tree.getLevel() + 1)
        current_tree.addChild(new_tree)
        current_tree = new_tree
    elif( re.search("^ *[e,E][n,N][d,D] *[d,D][o,O] *", line) ):
        current_tree.setIntervalEnd(i)
        current_tree = current_tree.getParent()

insertDecorations(code, root)

with open("output_code.F90", "w") as output_file:
    output_file.writelines(code)
