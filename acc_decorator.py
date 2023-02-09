import re
from interval_tree import IntervalTree

def insertDecorations(code, node, offset_lines = 0):
    insert_string = "\n"
    if ( node.get_data()[0] != None ):
        if ( node.get_level() == 1 ):
            if ( len( node.get_children()) == 0 ):
                insert_string = " VECTOR PRIVATE() IF(.false.)\n"
            else:
                insert_string = " PRIVATE() IF(.false.)\n"
        code.insert(node.get_data()[0] + offset_lines, loop_directives[0 + node.get_level() - 1] + insert_string)
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
